# SynFlict

A modern full-stack application built with Turborepo, SvelteKit, and GraphQL.

## What's Inside

This Turborepo includes the following packages/apps:

### Apps

- `web`: a [SvelteKit](https://kit.svelte.dev/) app with [Tailwind CSS](https://tailwindcss.com/)
- `api`: a [Fastify](https://www.fastify.io/) server with [GraphQL Yoga](https://the-guild.dev/graphql/yoga-server)

### Packages

- `config`: shared configuration (TypeScript, ESLint, Prettier)
- (future packages will be added here)

## Getting Started

### Prerequisites

- [Node.js](https://nodejs.org/en/) (v18 or newer)
- [pnpm](https://pnpm.io/) (v8.6.0 or newer)

### Installation

```bash
# Install dependencies
pnpm install
```

### Development

```bash
# Start all applications in development mode
pnpm dev

# Start only the web app
pnpm --filter web dev

# Start only the API
pnpm --filter api dev
```

### Building

```bash
# Build all applications
pnpm build

# Build only the web app
pnpm --filter web build

# Build only the API
pnpm --filter api build
```

### Testing

```bash
# Run all tests
pnpm test

# Run only web tests
pnpm --filter web test

# Run only API tests
pnpm --filter api test
```

### Linting and Type Checking

```bash
# Run linting on all packages
pnpm lint

# Run type checking on all packages
pnpm type-check
```

## Deployment

The project is set up with GitHub Actions for CI/CD. Every push to the main branch will trigger:

1. Linting
2. Type checking
3. Tests

## Project Structure

```
.
├── apps
│   ├── api              # Fastify + GraphQL Yoga API
│   └── web              # SvelteKit + Tailwind CSS web app
├── packages
│   └── config           # Shared configuration
├── .github
│   └── workflows        # GitHub Actions CI/CD
├── pnpm-workspace.yaml  # pnpm workspace configuration
└── turbo.json           # Turborepo configuration
```

## License

MIT
