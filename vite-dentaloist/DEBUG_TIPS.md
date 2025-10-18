# Debugging Tips

## Common Issues and Solutions

### 1. White Screen on Load
- Check browser console for errors
- Verify all dependencies are installed
- Check if backend is running
- Clear browser cache and localStorage

### 2. API Connection Failed
- Ensure backend is running on port 5000
- Check CORS configuration
- Verify VITE_API_URL environment variable
- Test backend health endpoint directly

### 3. Authentication Issues
- Clear localStorage tokens
- Check token expiration
- Verify route guards are working
- Test with admin direct login

### 4. TypeScript Errors
- Run `npm run type-check`
- Check for missing types
- Verify component props
- Update type definitions

### 5. Build Issues
- Run `npm run build` to check for errors
- Clear build cache with `npm run clean`
- Check for missing imports
- Verify all components are properly exported

## Development Tools

### Red Bug Icon
- Click the red bug icon in bottom-right for debug panel
- Check API status
- Clear storage
- Generate test data

### Browser DevTools
- Network tab: Check API calls
- Console: Look for errors
- Application tab: Check storage
- Elements: Inspect components

### React DevTools
- Install React DevTools browser extension
- Inspect component hierarchy
- Check props and state
- Profile performance