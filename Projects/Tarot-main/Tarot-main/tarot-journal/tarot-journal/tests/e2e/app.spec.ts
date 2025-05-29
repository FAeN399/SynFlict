import { test, expect } from '@playwright/test';

test('app shows welcome message', async ({ page }) => {
  // For Electron tests, this would need to be replaced with electron-playwright integration
  await page.goto('http://localhost:5173/');
  
  const heading = page.locator('h1');
  await expect(heading).toHaveText('Hello Offline');
});
