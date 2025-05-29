module.exports = {
  root: true,
  extends: ['config/eslint-preset.js'],
  parserOptions: {
    project: './tsconfig.json',
    tsconfigRootDir: __dirname
  },
  rules: {
    // Add any API-specific ESLint rules here
  }
};
