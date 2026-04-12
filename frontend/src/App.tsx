import { useState } from 'react'
import { ThemeProvider } from '@/components/theme-provider'
import { ModeToggle } from '@/components/mode-toggle'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion'
import { Send, Terminal, Loader2, Database } from 'lucide-react'

// Backend API URL configuration with fallback for local development
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  // --- State Management ---
  const [query, setQuery] = useState('')           // Stores the current user input
  const [isLoading, setIsLoading] = useState(false) // Tracks if an API request is in progress
  const [response, setResponse] = useState<any>(null)// Stores the successful API result
  const [error, setError] = useState('')           // Stores any error messages from the backend

  /**
   * Handles the submission of the natural language query.
   * Sends a POST request to the backend and handles JSON parsing and error cases.
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return

    setIsLoading(true)
    setError('')
    setResponse(null)

    try {
      // POST request to the /query endpoint with the user's natural language string
      const res = await fetch(`${API_BASE_URL}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      })
      
      let data;
      const text = await res.text();
      
      // Attempt to parse the response as JSON
      try {
        data = JSON.parse(text);
      } catch (parseErr) {
        // Handle non-JSON responses (often indicative of a server crash or 404)
        throw new Error(!res.ok ? `Server Error (${res.status}): ${text}` : `Invalid JSON response: ${text}`);
      }
      
      // Check for application-level errors returned in the JSON payload
      if (!res.ok || data.error) {
        throw new Error(data.error || `Failed to fetch query results (${res.status})`)
      }
      
      setResponse(data)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setIsLoading(false)
    }
  }

  /**
   * Dynamically renders the database results as a table.
   * Handles arrays of objects (table view) and empty results.
   */
  const renderData = (data: any) => {
    if (!data) return null;
    
    if (Array.isArray(data) && data.length > 0) {
      const keys = Object.keys(data[0]) // Extract column headers from the first record
      return (
        <div className="overflow-x-auto w-full border rounded-md mt-4">
          <table className="w-full text-sm text-left">
            <thead className="bg-muted text-muted-foreground uppercase">
              <tr>
                {keys.map(k => (
                  <th key={k} className="px-4 py-3 font-medium">{k}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {data.map((row: any, i: number) => (
                <tr key={i} className="border-t">
                  {keys.map(k => (
                    <td key={k + i} className="px-4 py-3">{String(row[k] ?? 'null')}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )
    } else if (Array.isArray(data) && data.length === 0) {
      return <div className="p-4 text-center text-muted-foreground bg-muted/20 rounded-md mt-4">No results found</div>
    } else {
      // Fallback for non-array results (e.g., single metrics or raw JSON)
      return (
        <div className="p-4 bg-muted/30 rounded-md mt-4">
          <pre className="whitespace-pre-wrap text-sm">{JSON.stringify(data, null, 2)}</pre>
        </div>
      )
    }
  }

  /**
   * Renders the LLM-generated business insight.
   * Handles both plain strings and structured JSON outputs from the explainer.
   */
  const renderExplanation = (exp: any) => {
    if (!exp) return null;
    let parsedExp = exp;
    
    // Attempt to parse stringified JSON if the backend returned it as a string
    if (typeof exp === 'string') {
      try {
        parsedExp = JSON.parse(exp);
      } catch (e) {
        // If parsing fails, treat it as a regular string
        return <p className="text-base text-card-foreground mt-2 font-medium">{exp}</p>;
      }
    }
    
    // Render the structured insight sections with custom styling
    if (typeof parsedExp === 'object' && parsedExp !== null) {
      return (
        <div className="flex flex-col gap-3 mt-4 text-sm w-full">
          {parsedExp.summary && (
            <div className="p-3 bg-primary/10 text-foreground rounded-r border-l-4 border-primary">
              <span className="font-bold block mb-1">Summary</span> 
              {parsedExp.summary}
            </div>
          )}
          {parsedExp.key_insight && (
            <div className="p-3 bg-accent/20 text-foreground rounded-r border-l-4 border-accent-foreground">
              <span className="font-bold block mb-1">Key Insight</span> 
              {parsedExp.key_insight}
            </div>
          )}
          {parsedExp.details && (
            <div className="p-3 bg-secondary text-foreground rounded-r border-l-4 border-secondary-foreground">
              <span className="font-bold block mb-1">Details</span> 
              {parsedExp.details}
            </div>
          )}
          {parsedExp.source && (
            <div className="text-xs text-muted-foreground italic mt-1">
              Source: {parsedExp.source}
            </div>
          )}
        </div>
      );
    }
    
    return <p className="text-base text-card-foreground mt-2 font-medium">{String(exp)}</p>;
  }

  return (
    <ThemeProvider defaultTheme="system" storageKey="vite-ui-theme">
      <div className="min-h-screen flex flex-col bg-background text-foreground">
        
        {/* Navigation Header */}
        <header className="border-b sticky top-0 bg-background/80 backdrop-blur z-10 w-full">
          <div className="container flex h-16 items-center justify-between mx-auto px-4">
            <div className="flex items-center gap-2">
              <Database className="w-6 h-6 text-primary" />
              <h1 className="text-xl font-bold tracking-tight">Code For Purpose</h1>
            </div>
            <ModeToggle />
          </div>
        </header>

        {/* Main Interface */}
        <main className="flex-1 container mx-auto px-4 py-8 mb-20 max-w-4xl flex flex-col items-center">
          
          {/* Hero Section */}
          <div className="w-full text-center mb-10 space-y-4">
            <h2 className="text-3xl font-extrabold tracking-tight lg:text-5xl">
              Ask your Data Anything
            </h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              Transform your natural language questions into database insights in seconds.
            </p>
          </div>

          {/* Search/Query Form */}
          <form onSubmit={handleSubmit} className="w-full relative shadow-sm max-w-2xl flex gap-2">
            <Input 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="e.g. Find all users who signed up last week..." 
              className="py-6 px-4 text-base rounded-full shadow-sm"
              disabled={isLoading}
            />
            <Button 
              type="submit" 
              disabled={isLoading || !query.trim()} 
              className="rounded-full h-auto px-6"
            >
              {isLoading ? <Loader2 className="w-5 h-5 animate-spin" /> : <Send className="w-5 h-5" />}
            </Button>
          </form>

          {/* Error display card */}
          {error && (
            <Card className="w-full mt-8 border-destructive/50 bg-destructive/10 text-destructive">
              <CardContent className="p-4">
                <p className="font-medium text-sm">{error}</p>
              </CardContent>
            </Card>
          )}

          {/* Results Area: Displays once an API response is received */}
          {response && (
            <div className="w-full mt-8 space-y-6 animate-in slide-in-from-bottom-4 duration-500 fade-in">
              
              {/* Main Results Card: Data Table */}
              <Card className="overflow-hidden border-primary/20 shadow-md">
                <CardContent className="pt-6 pb-2">
                  <div className="font-semibold text-lg border-b pb-2 mb-4">Results</div>
                  {renderData(response.data)}
                </CardContent>

                {/* Collapsible section for deep-dive details (SQL and Insights) */}
                {(response.explanation || response.sql) && (
                  <div className="px-6 pb-6 space-y-4 mt-2">
                    <Accordion type="multiple" className="w-full space-y-2">
                      
                      {/* Accordion for Business Insight (Explanation) */}
                      {response.explanation && (
                        <AccordionItem value="insight" className="border rounded-md px-4 bg-primary/5">
                          <AccordionTrigger className="text-sm font-medium hover:no-underline">
                            <div className="flex items-center gap-2 text-primary">
                              <Terminal className="w-4 h-4" />
                              View Insight
                            </div>
                          </AccordionTrigger>
                          <AccordionContent>
                            {renderExplanation(response.explanation)}
                          </AccordionContent>
                        </AccordionItem>
                      )}

                      {/* Accordion for Generated SQL Query (for transparency) */}
                      {response.sql && (
                        <AccordionItem value="sql" className="border rounded-md px-4 bg-muted/10">
                          <AccordionTrigger className="text-sm font-medium hover:no-underline">
                            View Generated SQL Query
                          </AccordionTrigger>
                          <AccordionContent>
                            <div className="bg-muted p-4 rounded-md overflow-x-auto relative mt-2 border">
                              <pre className="text-xs font-mono text-muted-foreground">
                                {response.sql}
                              </pre>
                            </div>
                          </AccordionContent>
                        </AccordionItem>
                      )}

                    </Accordion>
                  </div>
                )}
              </Card>

            </div>
          )}
        </main>

        {/* Branding Footer */}
        <footer className="border-t py-6 mt-auto">
          <div className="container mx-auto px-4 flex justify-between items-center text-sm text-muted-foreground">
            <p>Team Name - bottom3</p>
          </div>
        </footer>

      </div>
    </ThemeProvider>
  )
}

export default App
