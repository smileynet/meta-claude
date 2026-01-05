# Commit Message Examples

Example commit messages organized by change type. All follow the 50/72 rule, imperative mood, and WHAT/WHY focus.

## Feature Addition

```
Add user profile picture upload

Users requested ability to personalize their accounts.
Implements drag-and-drop upload with:
- Image resizing to 256x256
- Format validation (JPEG, PNG, WebP)
- S3 storage with CDN delivery

Closes #234
```

```
Add keyboard shortcuts for common actions

Power users navigate faster with keyboard. Added:
- Ctrl+K: Quick search
- Ctrl+N: New document
- Ctrl+S: Save (with visual feedback)

Shortcuts shown in menu items for discoverability.
```

## Bug Fix

```
Fix login failing for usernames with spaces

The URL encoding was stripping spaces from usernames,
causing authentication to fail for ~3% of users.
Now properly encodes all special characters.
```

```
Fix memory leak in WebSocket connection handler

Connections weren't being cleaned up on client disconnect,
causing server memory to grow ~50MB/hour under load.
Added cleanup in the disconnect event handler.
```

## Refactoring

```
Extract email sending into dedicated service

Email logic was scattered across 5 controllers, making
it hard to change providers or add templates. Moving
to EmailService centralizes configuration and enables
easier testing with mock provider.

No functional changes.
```

```
Simplify date formatting with shared utility

Multiple components had similar date formatting logic
with subtle inconsistencies. Created formatDate() utility
that handles all cases consistently.

Reduces bundle size by removing duplicate code.
```

## Performance

```
Add database index for user email lookups

Login queries were doing full table scans on the users
table (~2s for 1M users). Adding index on email column
reduces query time to <10ms.
```

```
Lazy load dashboard charts

Initial page load was 4s due to loading all chart data
upfront. Charts now load on scroll into viewport,
reducing initial load to under 1s.
```

## Documentation

```
Add API authentication guide

New developers were confused about obtaining and using
API keys. Added step-by-step guide with examples for
curl, Python, and JavaScript.
```

```
Update deployment instructions for Kubernetes

The previous Docker Compose instructions didn't cover
our new K8s setup. Added helm chart documentation and
environment configuration guide.
```

## Configuration

```
Update ESLint rules for stricter type checking

Added rules to catch common TypeScript errors earlier:
- no-explicit-any (prevents type erosion)
- strict-boolean-expressions (catches null checks)

Existing violations grandfathered with inline disables.
```

```
Add production environment configuration

Separates development and production settings for:
- Database connection pooling
- Cache TTL values
- Logging levels

Uses environment variables for sensitive values.
```

## Dependency Updates

```
Update React from 17 to 18

React 18 brings automatic batching and concurrent
features we'll use for the dashboard refresh.
Updated component lifecycle methods that changed.

Breaking: Requires Node 16+ (was 14+)
```

```
Remove unused lodash dependency

Only using lodash.debounce, which has a standalone
package. Reduces bundle size by 70KB.
```

## Test Changes

```
Add integration tests for payment flow

Payment bugs are high-impact. Added tests covering:
- Successful checkout
- Card decline handling
- Webhook processing
- Refund flow

Uses Stripe test mode with deterministic card numbers.
```

## Security

```
Fix XSS vulnerability in comment rendering

User comments weren't being sanitized before display,
allowing script injection. Now using DOMPurify to
sanitize all user-generated HTML content.

CVE-2024-XXXX
```

## Cleanup

```
Remove deprecated v1 API endpoints

The v1 API was deprecated 6 months ago and analytics
show zero usage in the past 30 days. Removing reduces
maintenance burden and attack surface.

BREAKING: v1 endpoints will return 410 Gone
```
