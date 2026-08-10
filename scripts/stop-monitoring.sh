#!/bin/bash
# Stop Health-AICare monitoring stack

set -e

echo "🛑 Stopping Health-AICare Monitoring Stack..."
echo ""

echo "Delegating to ./dev.sh (profiles-based monitoring stop)..."
echo ""

./dev.sh monitoring stop

echo ""
echo "🎉 Monitoring services stopped!"
