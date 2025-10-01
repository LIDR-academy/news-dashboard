# Frontend - React News Management Application

A modern React TypeScript frontend for the News Management system, built with feature-based architecture and comprehensive UI components.

## Tech Stack

- **React 19** with TypeScript for type safety
- **Vite** for fast development and building
- **TailwindCSS v4** for utility-first styling
- **Radix UI / shadcn/ui** for accessible, customizable components
- **React Query (TanStack Query)** for server state management
- **React Router v7** for client-side routing
- **dnd-kit** for drag-and-drop Kanban board functionality
- **Zod** for runtime validation and form schemas
- **Vitest + React Testing Library** for comprehensive testing

## Features

### News Management
- **Kanban Board**: Drag and drop news between status columns (To Read, Reading, Completed)
- **Mobile-Responsive**: Touch-friendly mobile view with tab navigation
- **News Creation**: Modal form with comprehensive validation
- **Real-time Filtering**: Filter by status, category, favorites, and date ranges
- **Favorites System**: Mark and filter favorite articles
- **Statistics Dashboard**: Real-time counters and progress tracking

### User Interface
- **Dark/Light Mode**: Theme switching with system preference detection
- **Responsive Design**: Mobile-first approach with desktop enhancements
- **Accessibility**: ARIA labels, keyboard navigation, screen reader support
- **Loading States**: Skeleton loaders and loading indicators
- **Error Handling**: User-friendly error messages and fallbacks

## Architecture

### Feature-Based Organization

The frontend follows a feature-based architecture for scalability and maintainability:

```
src/
├── features/           # Feature modules
│   ├── auth/          # Authentication feature
│   │   ├── components/    # Auth-specific components
│   │   ├── data/         # Schemas and services
│   │   └── hooks/        # Context, queries, mutations
│   └── news/          # News management feature
│       ├── components/    # News components (Board, Card, Modal, etc.)
│       ├── data/         # News schemas and API services
│       └── hooks/        # News context and React Query hooks
├── components/        # Shared components
│   ├── ui/           # Radix/shadcn UI components
│   └── *.tsx         # Shared application components
├── core/             # Core infrastructure
│   ├── data/         # API client, storage, query setup
│   └── hooks/        # Shared hooks
└── pages/            # Route components
```

### Component Patterns

#### Feature Context Pattern
Each feature exports a context provider and custom hook:

```typescript
// Feature context for state management
export const NewsProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  // ... context implementation
};

export const useNewsContext = (): NewsContextType => {
  // ... hook implementation
};
```

#### React Query Integration
Mutations and queries are organized by feature:

```typescript
// Mutations for data modification
export const useCreateNewsMutation = () => {
  return useMutation({
    mutationFn: (data: CreateNewsRequest) => newsService.createNews(data),
    onSuccess: () => queryClient.invalidateQueries(['news'])
  });
};

// Queries for data fetching
export const useUserNewsQuery = (filters: NewsFilters) => {
  return useQuery({
    queryKey: ['news', 'user', filters],
    queryFn: () => newsService.getUserNews(filters)
  });
};
```

## Development

### Prerequisites
- Node.js 18+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Development Scripts

```bash
# Development
npm run dev              # Start dev server with HMR

# Building
npm run build           # Build for production
npm run preview         # Preview production build

# Code Quality
npm run lint           # Run ESLint
npm run type-check     # Run TypeScript compiler

# Testing
npm test              # Run tests
npm run test:watch    # Run tests in watch mode
npm run test:coverage # Run tests with coverage
npm run test:ui       # Run tests with UI interface
```

## Testing

### Test Coverage
- **65+ Tests**: Comprehensive component and hook testing
- **Testing Library**: React Testing Library for component testing
- **Vitest**: Fast unit test runner with coverage reporting
- **User Event Testing**: Simulated user interactions
- **Accessibility Testing**: Screen reader and keyboard navigation tests

### Test Structure
```
src/
├── features/
│   └── news/
│       └── hooks/
│           └── __tests__/
│               ├── mutations/
│               └── queries/
└── components/
    └── __tests__/
        └── *.test.tsx
```

### Running Tests

```bash
# Run all tests
npm test

# Run specific test file
npm test -- --run src/features/auth/hooks/__tests__/mutations/useLogout.mutation.test.tsx

# Run tests for specific feature
npm test -- --run src/features/news/

# Run with coverage
npm run test:coverage

# Interactive test UI
npm run test:ui
```

## Configuration

### Environment Variables
Create a `.env` file in the frontend directory:

```env
VITE_API_BASE_URL=http://localhost:8000
VITE_APP_NAME=News Management
```

### TypeScript Configuration
The project uses strict TypeScript configuration with:
- Strict mode enabled
- Path mapping for clean imports (`@/` for src directory)
- Type checking for all files

## Expanding ESLint Configuration

For production applications, enable type-aware lint rules:

```js
export default tseslint.config([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...

      // Remove tseslint.configs.recommended and replace with this
      ...tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      ...tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      ...tseslint.configs.stylisticTypeChecked,

      // Other configs...
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```

You can also install [eslint-plugin-react-x](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-x) and [eslint-plugin-react-dom](https://github.com/Rel1cx/eslint-react/tree/main/packages/plugins/eslint-plugin-react-dom) for React-specific lint rules:

```js
// eslint.config.js
import reactX from 'eslint-plugin-react-x'
import reactDom from 'eslint-plugin-react-dom'

export default tseslint.config([
  globalIgnores(['dist']),
  {
    files: ['**/*.{ts,tsx}'],
    extends: [
      // Other configs...
      // Enable lint rules for React
      reactX.configs['recommended-typescript'],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ['./tsconfig.node.json', './tsconfig.app.json'],
        tsconfigRootDir: import.meta.dirname,
      },
      // other options...
    },
  },
])
```
