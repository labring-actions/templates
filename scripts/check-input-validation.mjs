#!/usr/bin/env node
// Checks `spec.inputs.<key>.validation` in every template.
//
// A template input may declare a list of regular expressions:
//
//   inputs:
//     admin_password:
//       description: Admin password. Use at least 8 characters.
//       type: string
//       required: true
//       validation:
//         - pattern: '.{8,}'
//
// Sealos rejects a deployment when a non-empty value does not match every pattern, so a
// wrong rule blocks real users. This script fails the pull request when a rule cannot
// work. It needs `js-yaml` (the parser the Template App Store uses):
//
//   npm install --no-save js-yaml@4.3.2
//   node scripts/check-input-validation.mjs [file ...]
//
// With no arguments it checks template/*/index.yaml and template/*.yaml.

import fs from 'node:fs';
import path from 'node:path';
import yaml from 'js-yaml';

const MAX_VALUE_LENGTH = 1024;
const VALIDATED_TYPES = new Set(['string', 'number']);

const root = path.resolve(path.dirname(new URL(import.meta.url).pathname), '..');

function templateFiles() {
  const dir = path.join(root, 'template');
  const files = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const file = entry.isDirectory()
      ? path.join(dir, entry.name, 'index.yaml')
      : path.join(dir, entry.name);
    if (file.endsWith('.yaml') && fs.existsSync(file)) files.push(file);
  }
  return files.sort();
}

// Later documents hold `${{ if(...) }}` lines that are not YAML until the template is
// rendered, so only the leading documents up to the Template are parsed.
function readTemplate(file) {
  for (const document of fs.readFileSync(file, 'utf8').split(/^---[ \t]*\r?\n/m)) {
    if (!document.trim()) continue;
    const parsed = yaml.load(document);
    return parsed?.kind === 'Template' ? parsed : undefined;
  }
  return undefined;
}

function isPlainObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value);
}

// True when one of `chars` appears as regex syntax: not escaped, not inside a [...] class.
function usesSyntax(pattern, chars) {
  const outsideClasses = pattern.replace(/\\.|\[(?:\\.|[^\]\\])*\]/gs, (match) =>
    match.startsWith('[') ? '' : '__'
  );
  return [...chars].some((char) => outsideClasses.includes(char));
}

function checkInput(key, input) {
  const errors = [];
  const warnings = [];
  const { validation } = input;

  if (!Array.isArray(validation) || validation.length === 0) {
    errors.push('`validation` must be a non-empty list of `- pattern: ...` rules');
    return { errors, warnings };
  }

  const type = String(input.type ?? 'string').trim().toLowerCase();
  if (!VALIDATED_TYPES.has(type)) {
    errors.push(`\`validation\` is only supported on string and number inputs, not "${type}"`);
  }
  if (typeof input.description !== 'string' || !input.description.trim()) {
    errors.push('an input with `validation` needs a `description` that states the requirement');
  }

  const regexes = [];
  validation.forEach((rule, index) => {
    const label = `validation[${index}]`;
    if (!isPlainObject(rule) || typeof rule.pattern !== 'string' || rule.pattern === '') {
      errors.push(`${label} must be \`pattern: <non-empty string>\``);
      return;
    }
    const extra = Object.keys(rule).filter((name) => name !== 'pattern');
    if (extra.length > 0) {
      errors.push(`${label} has unsupported keys: ${extra.join(', ')} (only \`pattern\` is allowed)`);
    }
    try {
      regexes.push(new RegExp(rule.pattern, 'u'));
    } catch (error) {
      errors.push(`${label} does not compile: ${error.message}`);
      return;
    }
    if (usesSyntax(rule.pattern, '+*') && !usesSyntax(rule.pattern, '^$')) {
      warnings.push(
        `${label} "${rule.pattern}" has no ^ or $. A pattern matches anywhere in the value; ` +
          'write ^...$ if the whole value must match'
      );
    }
  });

  const fallback = input.default;
  const isStatic =
    fallback !== undefined && fallback !== null && fallback !== '' && !String(fallback).includes('${{');
  if (isStatic) {
    const value = String(fallback);
    if (Array.from(value).length > MAX_VALUE_LENGTH) {
      errors.push(`default is longer than ${MAX_VALUE_LENGTH} characters and is always rejected`);
    }
    for (const regex of regexes) {
      if (!regex.test(value)) {
        errors.push(`default "${value}" does not match its own rule "${regex.source}"`);
      }
    }
  }

  return { errors, warnings };
}

function annotate(level, file, message) {
  const relative = path.relative(root, file);
  const prefix = process.env.GITHUB_ACTIONS ? `::${level} file=${relative}::` : `${level}: `;
  console.log(`${prefix}${relative}: ${message}`);
}

const files = process.argv.length > 2 ? process.argv.slice(2).map((f) => path.resolve(f)) : templateFiles();
let errorCount = 0;
let warningCount = 0;
let ruleCount = 0;

for (const file of files) {
  let template;
  try {
    template = readTemplate(file);
  } catch (error) {
    annotate('error', file, `cannot parse the Template document: ${error.message}`);
    errorCount += 1;
    continue;
  }
  const inputs = template?.spec?.inputs;
  if (!isPlainObject(inputs)) continue;

  for (const [key, input] of Object.entries(inputs)) {
    if (!isPlainObject(input) || !('validation' in input)) continue;
    ruleCount += 1;
    const { errors, warnings } = checkInput(key, input);
    for (const message of errors) annotate('error', file, `inputs.${key}: ${message}`);
    for (const message of warnings) annotate('warning', file, `inputs.${key}: ${message}`);
    errorCount += errors.length;
    warningCount += warnings.length;
  }
}

console.log(
  `Checked ${files.length} template(s), ${ruleCount} input(s) with validation: ` +
    `${errorCount} error(s), ${warningCount} warning(s).`
);
process.exit(errorCount > 0 ? 1 : 0);
