#!/bin/bash
#
# 一次性清理 MongoDB、PostgreSQL、MySQL 数据库日志的脚本
# 用于 Kubernetes 环境
#

set -o pipefail

MAX_PARALLEL=20  # 最大并行任务数

process_mongodb() {
  local namespace=$1
  local pod=$2
  local cluster_name=$(echo "$pod" | sed 's/-[0-9]*$//' | sed 's/-mongodb$//')
  
  local username="" password="" secret_name=""
  
  # 尝试第一种 secret
  secret_name="${cluster_name}-mongodb-account-root"
  if kubectl get secret -n "$namespace" "$secret_name" --request-timeout=5s >/dev/null 2>&1; then
    username=$(kubectl get secret -n "$namespace" "$secret_name" -o jsonpath='{.data.username}' 2>/dev/null | base64 -d 2>/dev/null)
    password=$(kubectl get secret -n "$namespace" "$secret_name" -o jsonpath='{.data.password}' 2>/dev/null | base64 -d 2>/dev/null)
  fi
  
  # 如果第一种失败，尝试第二种
  if [ -z "$username" ] || [ -z "$password" ]; then
    secret_name="${cluster_name}-conn-credential"
    if kubectl get secret -n "$namespace" "$secret_name" --request-timeout=5s >/dev/null 2>&1; then
      username=$(kubectl get secret -n "$namespace" "$secret_name" -o jsonpath='{.data.username}' 2>/dev/null | base64 -d 2>/dev/null)
      password=$(kubectl get secret -n "$namespace" "$secret_name" -o jsonpath='{.data.password}' 2>/dev/null | base64 -d 2>/dev/null)
    fi
  fi
  
  if [ -z "$username" ] || [ -z "$password" ]; then
    echo "  Warning: No credentials for $namespace/$pod (cluster: $cluster_name)"
    return 0
  fi
  
  echo "  Rotating $namespace/$pod (secret: $secret_name)..."
  kubectl exec -n "$namespace" "$pod" -c mongodb --request-timeout=30s -- bash -c ': > /data/mongodb/logs/mongodb.log' 2>/dev/null || true
  kubectl exec -n "$namespace" "$pod" -c mongodb --request-timeout=30s -- mongosh --quiet -u "$username" -p "$password" --authenticationDatabase admin --eval 'db.adminCommand({logRotate: 1})' 2>/dev/null || true
}

process_postgresql() {
  local namespace=$1
  local pod=$2
  echo "  Clearing $namespace/$pod..."
  kubectl exec -n "$namespace" "$pod" -c postgresql --request-timeout=30s -- bash -c ': > /home/postgres/pgdata/pgroot/pg_log/postgresql.log' 2>/dev/null || true
  kubectl exec -n "$namespace" "$pod" -c postgresql --request-timeout=30s -- psql -U postgres -c "SELECT pg_reload_conf();" 2>/dev/null || true
}

process_mysql() {
  local namespace=$1
  local pod=$2
  echo "  Clearing $namespace/$pod..."
  kubectl exec -n "$namespace" "$pod" -c mysql --request-timeout=30s -- bash -c ': > /data/mysql/log/slow-query.log' 2>/dev/null || true
  kubectl exec -n "$namespace" "$pod" -c mysql --request-timeout=30s -- bash -c ': > /data/mysql/log/mysqld-error.log' 2>/dev/null || true
}

export -f process_mongodb
export -f process_postgresql
export -f process_mysql

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting one-time DB log cleanup..."

# MongoDB
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Clearing MongoDB logs..."
mongo_pods=$(kubectl get pod -A --no-headers 2>/dev/null | grep -E '\-mongodb-[0-9]+\s' || true)
job_count=0
while IFS= read -r line; do
  [ -z "$line" ] && continue
  namespace=$(echo "$line" | awk '{print $1}')
  pod=$(echo "$line" | awk '{print $2}')
  process_mongodb "$namespace" "$pod" &
  job_count=$((job_count + 1))
  [ $job_count -ge $MAX_PARALLEL ] && { wait -n 2>/dev/null || wait; job_count=$((job_count - 1)); }
done <<< "$mongo_pods"
wait

# PostgreSQL
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Clearing PostgreSQL logs..."
pg_pods=$(kubectl get pod -A --no-headers 2>/dev/null | grep -E '\-postgresql-[0-9]+\s' || true)
job_count=0
while IFS= read -r line; do
  [ -z "$line" ] && continue
  namespace=$(echo "$line" | awk '{print $1}')
  pod=$(echo "$line" | awk '{print $2}')
  process_postgresql "$namespace" "$pod" &
  job_count=$((job_count + 1))
  [ $job_count -ge $MAX_PARALLEL ] && { wait -n 2>/dev/null || wait; job_count=$((job_count - 1)); }
done <<< "$pg_pods"
wait

# MySQL
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Clearing MySQL logs..."
mysql_pods=$(kubectl get pod -A --no-headers 2>/dev/null | grep -E '\-mysql-[0-9]+\s' || true)
job_count=0
while IFS= read -r line; do
  [ -z "$line" ] && continue
  namespace=$(echo "$line" | awk '{print $1}')
  pod=$(echo "$line" | awk '{print $2}')
  process_mysql "$namespace" "$pod" &
  job_count=$((job_count + 1))
  [ $job_count -ge $MAX_PARALLEL ] && { wait -n 2>/dev/null || wait; job_count=$((job_count - 1)); }
done <<< "$mysql_pods"
wait

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Done. All database logs cleared."
