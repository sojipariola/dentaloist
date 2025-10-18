import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  // Run tests locally in development
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:5173',
    reuseExistingServer: !process.env.CI,
  },
  use: {
    baseURL: 'http://localhost:5173',
  },
  testDir: './tests/e2e',
});
