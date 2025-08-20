# QDPI UI Playground

This directory contains the source code for the QDPI UI Playground, developed by Gemini.

## How to Apply the Patch

To apply the changes to your `src` directory, run the following command from the root of the project:

```bash
git apply --index contrib/gemini/patches/qdpi-ui.patch
```

If you encounter any conflicts, you can try a 3-way merge:

```bash
git apply --3way contrib/gemini/patches/qdpi-ui.patch
```

## How to Run

After applying the patch, install the dependencies:

```bash
pnpm install
```

Then, run the development server:

```bash
pnpm dev
```

Open your browser to `http://localhost:5173/qdpi` to see the playground.

## Environment Variables

To connect to a different backend, you can set the following environment variable in a `.env` file:

```
VITE_API_BASE_URL=http://localhost:8000
```
