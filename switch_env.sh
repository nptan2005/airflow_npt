#!/bin/bash

if [[ "$OSTYPE" == "darwin"* ]]; then
  cp .env.mac .env
  echo "✅ Loaded macOS .env"
else
  cp .env.windows .env
  echo "✅ Loaded Windows .env"
fi