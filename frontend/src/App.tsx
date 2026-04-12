import { useState } from 'react'
import { ThemeProvider } from '@/components/theme-provider'
import { ModeToggle } from '@/components/mode-toggle'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from '@/components/ui/accordion'
import { Send, Terminal, Loader2, Database } from 'lucide-react'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [query, setQuery] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [response, setResponse] = useState<any>(null)
  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return

    setIsLoading(true)
    setError('')
    setResponse(null)

    try {
      const res = await fetch(`${API_BASE_URL}query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query })
      })
      
      let data;
      const text = await res.text();
      
      try {
        data = JSON.parse(text);
      } catch (parseErr) {
        throw new Error(!res.ok ? `Server Error (${res.status}): ${text}` : `Invalid JSON response: ${text}`);
      }
      
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

  // Render dynamic data as a table if it's an array of objects
  const renderData = (data: any) => {
    if (!data) return null;
    
    if (Array.isArray(data) && data.length > 0) {
      const keys = Object.keys(data[0])
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
      return (
        <div className="p-4 bg-muted/30 rounded-md mt-4">
          <pre className="whitespace-pre-wrap text-sm">{JSON.stringify(data, null, 2)}</pre>
        </div>
      )
    }
  }

  const renderExplanation = (exp: any) => {
    if (!exp) return null;
    let parsedExp = exp;
    
    // Attempt to parse stringified JSON
    if (typeof exp === 'string') {
      try {
        parsedExp = JSON.parse(exp);
      } catch (e) {
        // Just a regular string
        return <p className="text-base text-card-foreground mt-2 font-medium">{exp}</p>;
      }
    }
    
    // Render the structured JSON output nicely
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
        
        {/* Header */}
        <header className="border-b sticky top-0 bg-background/80 backdrop-blur z-10 w-full">
          <div className="container flex h-16 items-center justify-between mx-auto px-4">
            <div className="flex items-center gap-2">
              <Database className="w-6 h-6 text-primary" />
              <h1 className="text-xl font-bold tracking-tight">Code For Purpose</h1>
            </div>
            <ModeToggle />
          </div>
        </header>

        {/* Main Content */}
        <main className="flex-1 container mx-auto px-4 py-8 mb-20 max-w-4xl flex flex-col items-center">
          
          <div className="w-full text-center mb-10 space-y-4">
            <h2 className="text-3xl font-extrabold tracking-tight lg:text-5xl">
              Ask your Data Anything
            </h2>
            <p className="text-muted-foreground text-lg max-w-2xl mx-auto">
              Transform your natural language questions into database insights in seconds.
            </p>
          </div>

          {/* Form */}
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

          {/* Error display */}
          {error && (
            <Card className="w-full mt-8 border-destructive/50 bg-destructive/10 text-destructive">
              <CardContent className="p-4">
                <p className="font-medium text-sm">{error}</p>
              </CardContent>
            </Card>
          )}

          {/* Results Display */}
          {response && (
            <div className="w-full mt-8 space-y-6 animate-in slide-in-from-bottom-4 duration-500 fade-in">
              
              <Card className="overflow-hidden border-primary/20 shadow-md">
                <CardContent className="pt-6 pb-2">
                  <div className="font-semibold text-lg border-b pb-2 mb-4">Results</div>
                  {renderData(response.data)}
                </CardContent>

                {(response.explanation || response.sql) && (
                  <div className="px-6 pb-6 space-y-4 mt-2">
                    <Accordion type="multiple" className="w-full space-y-2">
                      
                      {/* Accordion for Insight */}
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

                      {/* Accordion for SQL Query */}
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

        {/* Footer */}
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
