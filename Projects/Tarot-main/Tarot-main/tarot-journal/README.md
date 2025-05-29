# Tarot Journal

An offline-first tarot journal application built with Electron and React.

## Development

```bash
# Install dependencies
npm install

# Start the dev server
npm run dev
```

## Building and Packaging

```bash
# Build the application
npm run build

# Package for your current platform
npm run package

# Package for specific platforms
npm run package:win  # Windows
npm run package:mac  # macOS
npm run package:linux  # Linux
```

## Code Signing

For production builds, you'll need to set up code signing:

1. Obtain a code signing certificate (.pfx file)
2. Place it in the root directory as `certificate.pfx`
3. Set the certificate password as an environment variable:
   ```
   export CERTIFICATE_PASSWORD=your-password-here
   ```
4. Run the package command

## Testing

```bash
# Run unit tests
npm run test:unit

# Run end-to-end tests
npm run test:e2e
```
