#!/bin/bash

# ClickHouse 连通性测试脚本
# 用法: ./test_clickhouse.sh [host] [port] [user] [password]

# 默认配置
HOST="${1:-localhost}"
PORT="${2:-8123}"
USER="${3:-default}"
PASSWORD="${4:-}"

echo "========================================"
echo "ClickHouse 连通性测试"
echo "========================================"
echo "Host: $HOST"
echo "Port: $PORT"
echo "User: $USER"
echo "Password: ${PASSWORD:-(无密码)}"
echo "========================================"

# 测试1: 检查端口连通性
echo -e "\n[1/4] 检查端口连通性..."
if nc -z -w 5 "$HOST" "$PORT" 2>/dev/null; then
    echo "✅ 端口 $PORT 可访问"
else
    echo "❌ 无法连接到 $HOST:$PORT"
    echo "   请检查:"
    echo "   - ClickHouse 是否启动"
    echo "   - 防火墙是否允许端口 $PORT"
    echo "   - 主机名/IP 是否正确"
    exit 1
fi

# 测试2: HTTP 健康检查
echo -e "\n[2/4] HTTP 健康检查..."
HEALTH_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" "http://$HOST:$PORT/ping" 2>/dev/null)
if [ "$HEALTH_RESPONSE" = "200" ]; then
    echo "✅ HTTP 健康检查通过"
else
    echo "❌ HTTP 健康检查失败 (HTTP $HEALTH_RESPONSE)"
fi

# 测试3: 执行简单查询
echo -e "\n[3/4] 执行测试查询..."
if [ -n "$PASSWORD" ]; then
    AUTH="--user $USER:$PASSWORD"
else
    AUTH="--user $USER"
fi

QUERY_RESULT=$(curl -s $AUTH "http://$HOST:$PORT/?query=SELECT%201" 2>/dev/null)
if [ "$QUERY_RESULT" = "1" ]; then
    echo "✅ 查询测试通过"
else
    echo "❌ 查询测试失败"
    echo "   响应: $QUERY_RESULT"
fi

# 测试4: 获取版本信息
echo -e "\n[4/4] 获取 ClickHouse 版本..."
VERSION=$(curl -s $AUTH "http://$HOST:$PORT/?query=SELECT%20version()" 2>/dev/null)
if [ -n "$VERSION" ]; then
    echo "✅ ClickHouse 版本: $VERSION"
else
    echo "❌ 无法获取版本信息"
fi

# 附加信息: 获取数据库列表
echo -e "\n========================================"
echo "附加信息: 数据库列表"
echo "========================================"
DATABASES=$(curl -s $AUTH "http://$HOST:$PORT/?query=SHOW%20DATABASES" 2>/dev/null)
if [ -n "$DATABASES" ]; then
    echo "$DATABASES"
else
    echo "(无法获取数据库列表)"
fi

echo -e "\n========================================"
echo "测试完成!"
echo "========================================"
