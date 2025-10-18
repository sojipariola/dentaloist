# DentalSys - Next.js Frontend

A world-class, modern frontend for your dental/medical clinic management system built with Next.js, TypeScript, and Tailwind CSS.

## Features

- ✅ Stunning graphical homepage with animations
- ✅ Role-based dashboards (Dentist, Admin, Lab Tech, etc.)
- ✅ Drag-and-drop widget system
- ✅ Appointment calendar and patient management
- ✅ Responsive design with light/dark theme
- ✅ TypeScript interfaces matching your Flask models
- ✅ API service layer wired to Flask endpoints
- ✅ Authentication & permission system
- ✅ Zustand for state management

## Getting Started

1. Clone or download this repository
2. Install dependencies:
   ```bash
   npm install
3. Start development server:
    ```bash
    npm run dev
4. Open [http://localhost:3000](http://localhost:3000) in your browser
5. Configure environment variables in `.env.local`:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:5000

   Project Structure
- `app/` - Next.js app directory with pages and components
- `lib/` - API service layer and custom hooks
- `types/` - TypeScript interfaces for models
- `store/` - Zustand state management stores
- `styles/` - Global and theme CSS files
- `public/` - Static assets like images and favicon

src/
├── app/              # Next.js App Router pages
├── components/       # Reusable UI components
├── lib/              # Utility functions, API services, hooks
├── types/            # TypeScript interfaces
├── styles/           # Global styles
├── store/            # Zustand state management
└── public/           # Static assets

Customization
Modify tailwind.config.js to change colors and theme
Add new pages in src/app/
Extend API modules in src/lib/api/
Add new components in src/components/
License
This template is provided as-is for educational and development purposes.

yarn add next-themes
yarn add @radix-ui/react-slot
yarn add class-variance-authority
yarn add clsx tailwind-merge



# Backup your important files first
cp package.json package.json.backup
cp tailwind.config.js tailwind.config.js.backup
cp postcss.config.js postcss.config.js.backup

# Remove node_modules and lock files
rm -rf node_modules yarn.lock

# Reinstall everything
yarn install

# Make sure Tailwind is properly installed
yarn add -D tailwindcss@latest postcss@latest autoprefixer@latest

# Clear cache and try again
rm -rf .next node_modules/.cache
yarn dev