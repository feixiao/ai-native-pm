#!/usr/bin/env node

import { run } from '../src/index.mjs';

run().catch((err) => {
  console.error('\n❌ Unhandled error:', err.message || err);
  process.exit(1);
});
