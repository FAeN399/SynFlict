<script>
  import { Card, Alert } from '@synflict/ui';
</script>

<div class="container mx-auto px-4 py-8 max-w-4xl">
  <h1 class="text-4xl font-bold text-gray-800 mb-8">SynFlict Documentation</h1>
  
  <Card padding="lg" shadow="md" rounded="md" border={true} class="mb-8">
    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Project Overview</h2>
    <p class="text-gray-700 mb-4">
      SynFlict is a modern full-stack application built with a monorepo architecture using Turborepo.
      This approach allows us to manage multiple packages and applications in a single repository,
      sharing code and configuration while maintaining separation of concerns.
    </p>
    <Alert type="info" class="mt-4">
      <p>This documentation provides an overview of the project structure, architecture, and development workflow.</p>
    </Alert>
  </Card>
  
  <h2 class="text-2xl font-semibold text-gray-800 mb-4">Project Structure</h2>
  
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
    <Card padding="md" shadow="md" rounded="md" border={true}>
      <h3 class="text-xl font-semibold text-gray-800 mb-3">Apps</h3>
      <div class="space-y-3">
        <div>
          <h4 class="font-medium text-gray-800">web</h4>
          <p class="text-gray-600 text-sm">SvelteKit frontend application with Tailwind CSS</p>
        </div>
        <div>
          <h4 class="font-medium text-gray-800">api</h4>
          <p class="text-gray-600 text-sm">Fastify server with GraphQL Yoga</p>
        </div>
      </div>
    </Card>
    
    <Card padding="md" shadow="md" rounded="md" border={true}>
      <h3 class="text-xl font-semibold text-gray-800 mb-3">Packages</h3>
      <div class="space-y-3">
        <div>
          <h4 class="font-medium text-gray-800">config</h4>
          <p class="text-gray-600 text-sm">Shared configuration (TypeScript, ESLint, Prettier)</p>
        </div>
        <div>
          <h4 class="font-medium text-gray-800">ui</h4>
          <p class="text-gray-600 text-sm">Shared UI component library for Svelte applications</p>
        </div>
      </div>
    </Card>
  </div>
  
  <Card padding="lg" shadow="md" rounded="md" border={true} class="mb-8">
    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Architecture</h2>
    
    <div class="mb-6">
      <h3 class="text-xl font-semibold text-gray-800 mb-3">Frontend (SvelteKit)</h3>
      <ul class="list-disc pl-5 space-y-2 text-gray-700">
        <li>Built with SvelteKit for server-side rendering and routing</li>
        <li>Styled with Tailwind CSS for responsive design</li>
        <li>Uses Apollo Client for GraphQL data fetching</li>
        <li>Imports shared UI components from the UI package</li>
        <li>Follows a page-based routing structure</li>
      </ul>
    </div>
    
    <div class="mb-6">
      <h3 class="text-xl font-semibold text-gray-800 mb-3">Backend (Fastify + GraphQL)</h3>
      <ul class="list-disc pl-5 space-y-2 text-gray-700">
        <li>Built with Fastify for high-performance REST endpoints</li>
        <li>GraphQL Yoga for the GraphQL API layer</li>
        <li>Simple in-memory database for demonstration purposes</li>
        <li>Structured with a clean separation of concerns</li>
        <li>Provides a GraphQL schema with queries and mutations</li>
      </ul>
    </div>
    
    <div>
      <h3 class="text-xl font-semibold text-gray-800 mb-3">Shared UI Library</h3>
      <ul class="list-disc pl-5 space-y-2 text-gray-700">
        <li>Reusable Svelte components with TypeScript support</li>
        <li>Styled with Tailwind CSS for consistent design</li>
        <li>Includes common UI elements like buttons, cards, inputs, and alerts</li>
        <li>Used by the web application for a consistent UI</li>
      </ul>
    </div>
  </Card>
  
  <Card padding="lg" shadow="md" rounded="md" border={true} class="mb-8">
    <h2 class="text-2xl font-semibold text-gray-800 mb-4">Development Workflow</h2>
    
    <div class="space-y-4">
      <div>
        <h3 class="text-xl font-semibold text-gray-800 mb-2">Installation</h3>
        <div class="bg-gray-800 text-white p-4 rounded-md overflow-x-auto">
          <pre><code>pnpm install</code></pre>
        </div>
      </div>
      
      <div>
        <h3 class="text-xl font-semibold text-gray-800 mb-2">Development</h3>
        <div class="bg-gray-800 text-white p-4 rounded-md overflow-x-auto">
          <pre><code># Start all applications
pnpm dev

# Start only the web app
pnpm --filter web dev

# Start only the API
pnpm --filter api dev</code></pre>
        </div>
      </div>
      
      <div>
        <h3 class="text-xl font-semibold text-gray-800 mb-2">Building</h3>
        <div class="bg-gray-800 text-white p-4 rounded-md overflow-x-auto">
          <pre><code># Build all applications
pnpm build

# Build only the web app
pnpm --filter web build

# Build only the API
pnpm --filter api build</code></pre>
        </div>
      </div>
      
      <div>
        <h3 class="text-xl font-semibold text-gray-800 mb-2">Testing</h3>
        <div class="bg-gray-800 text-white p-4 rounded-md overflow-x-auto">
          <pre><code># Run all tests
pnpm test

# Run only web tests
pnpm --filter web test

# Run only API tests
pnpm --filter api test</code></pre>
        </div>
      </div>
    </div>
  </Card>
  
  <Card padding="lg" shadow="md" rounded="md" border={true}>
    <h2 class="text-2xl font-semibold text-gray-800 mb-4">CI/CD Pipeline</h2>
    
    <p class="text-gray-700 mb-4">
      The project uses GitHub Actions for continuous integration and deployment.
      Every push to the main branch triggers the following workflow:
    </p>
    
    <ol class="list-decimal pl-5 space-y-2 text-gray-700 mb-6">
      <li>Install dependencies with pnpm</li>
      <li>Run linting across all packages and applications</li>
      <li>Run type checking for TypeScript files</li>
      <li>Execute tests with Vitest</li>
    </ol>
    
    <Alert type="success">
      <p>The CI pipeline runs on both Ubuntu and macOS environments to ensure cross-platform compatibility.</p>
    </Alert>
  </Card>
  
  <div class="mt-8 text-center">
    <a href="/" class="text-blue-600 hover:text-blue-800 font-medium">← Back to Home</a>
  </div>
</div>
