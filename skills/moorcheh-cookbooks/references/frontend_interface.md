# Frontend Interface

Build a Next.js frontend to interact with a Moorcheh backend. Includes chat UI and search interfaces.

## Prerequisites

- A running Moorcheh backend (any cookbook above)
- Node.js 18+
- npm or yarn

## Quick Start

```bash
npx create-next-app@latest moorcheh-frontend --typescript --tailwind --app
cd moorcheh-frontend
npm install
```

## Project Structure

```
moorcheh-frontend/
├── app/
│   ├── layout.tsx
│   ├── page.tsx          # Main search/chat page
│   ├── api/
│   │   ├── search/route.ts
│   │   └── answer/route.ts
│   └── components/
│       ├── SearchBar.tsx
│       ├── ResultCard.tsx
│       └── ChatWindow.tsx
├── .env.local
└── package.json
```

## Environment Variables

```env
# .env.local
MOORCHEH_API_KEY=your-api-key-here
MOORCHEH_BASE_URL=https://api.moorcheh.ai/v1
NEXT_PUBLIC_APP_TITLE=Moorcheh Search
```

## API Routes

### Search Route

```typescript
// app/api/search/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const { query, namespaces, top_k } = await request.json();

  const response = await fetch(`${process.env.MOORCHEH_BASE_URL}/search`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': process.env.MOORCHEH_API_KEY!,
    },
    body: JSON.stringify({ query, namespaces, top_k: top_k || 10 }),
  });

  const data = await response.json();
  return NextResponse.json(data);
}
```

### Answer Route

```typescript
// app/api/answer/route.ts
import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  const { query, namespace, chatHistory } = await request.json();

  const response = await fetch(`${process.env.MOORCHEH_BASE_URL}/answer`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': process.env.MOORCHEH_API_KEY!,
    },
    body: JSON.stringify({ query, namespace, chatHistory }),
  });

  const data = await response.json();
  return NextResponse.json(data);
}
```

## Key Guidelines

- Always proxy Moorcheh API calls through Next.js API routes — never expose `MOORCHEH_API_KEY` to the client
- Use streaming for long AI-generated answers when possible
- Add loading states for search and answer generation
- Implement error handling with user-friendly messages
- Consider debouncing search input for better UX
