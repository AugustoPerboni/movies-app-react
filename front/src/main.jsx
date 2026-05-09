import './css/index.css'
import '@copilotkit/react-ui/styles.css'

import { CopilotKit } from '@copilotkit/react-core'
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'

import App from './App.jsx'
import { AuthProvider } from './context/AuthContext.jsx'

createRoot(document.getElementById('root')).render(
  <CopilotKit runtimeUrl="http://localhost:3001/api/copilotkit" agent="agno_agent">
    <StrictMode>
      <BrowserRouter>
        <AuthProvider>
          <App />
        </AuthProvider>
      </BrowserRouter>
    </StrictMode>
  </CopilotKit>,
)
