import { test, expect } from '@playwright/test';

test('app loads and shows welcome message', async ({ page }) => {
  // Navigate to the app
  await page.goto('/');
  
  // Wait for the page to load
  await page.waitForLoadState('networkidle');
  
  // Check for the main heading
  const heading = page.locator('h1');
  await expect(heading).toHaveText('Hello Offline');
  
  // Check for the subtitle
  const subtitle = page.locator('.subtitle');
  await expect(subtitle).toHaveText('Welcome to Tarot Journal');
  
  // Test the counter button functionality
  const button = page.locator('button');
  await expect(button).toContainText('Count is 0');
  
  // Click the button and verify count increases
  await button.click();
  await expect(button).toContainText('Count is 1');
  
  // Click again to verify it continues incrementing
  await button.click();
  await expect(button).toContainText('Count is 2');
});

test('search bar is present', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');
  
  // Just check that the search bar exists without testing input
  const searchBar = page.locator('.search-bar');
  await expect(searchBar).toBeVisible();
  
  const searchInput = page.locator('input[type="text"]');
  await expect(searchInput).toBeVisible();
});

test('version info section is displayed', async ({ page }) => {
  await page.goto('/');
  await page.waitForLoadState('networkidle');
  
  // Check version info section
  const versionInfo = page.locator('.version-info');
  await expect(versionInfo).toBeVisible();
  
  // Check that it contains the expected labels
  await expect(versionInfo.locator('p')).toHaveText('Using:');
  await expect(versionInfo.locator('li').first()).toContainText('Chrome');
  await expect(versionInfo.locator('li').nth(1)).toContainText('Node');
  await expect(versionInfo.locator('li').nth(2)).toContainText('Electron');
});
