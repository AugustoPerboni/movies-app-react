import process from 'node:process'

import { AgnoAgent } from '@ag-ui/agno'
import {
  CopilotRuntime,
  copilotRuntimeNodeExpressEndpoint,
  ExperimentalEmptyAdapter,
} from '@copilotkit/runtime'
import express from 'express'

const app = express()
const port = process.env.COPILOT_RUNTIME_PORT || 3001
const allowedOriginPattern = /^http:\/\/(localhost|127\.0\.0\.1):\d+$/

const runtime = new CopilotRuntime({
  agents: {
    agno_agent: new AgnoAgent({
      url: process.env.AGNO_URL || 'http://localhost:8000/agui',
    }),
  },
})

const handler = copilotRuntimeNodeExpressEndpoint({
  runtime,
  serviceAdapter: new ExperimentalEmptyAdapter(),
  endpoint: '/api/copilotkit',
  cors: {
    origin: (origin) => {
      if (!origin || allowedOriginPattern.test(origin)) {
        return origin
      }

      return null
    },
    credentials: true,
  },
})

app.use((req, res, next) => {
  if (req.path === '/api/copilotkit' || req.path.startsWith('/api/copilotkit/')) {
    return handler(req, res)
  }
  next()
})

app.listen(port, () => {
  console.warn(`Copilot runtime on http://localhost:${port}/api/copilotkit`)
})
