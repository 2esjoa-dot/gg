import { useState, useEffect, useCallback, useRef } from 'react'

interface UsePollingOptions {
  interval?: number
  enabled?: boolean
}

export function usePolling<T>(
  fetcher: () => Promise<T>,
  { interval = 30000, enabled = true }: UsePollingOptions = {}
) {
  const [data, setData] = useState<T | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState<Error | null>(null)
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null)

  const fetchData = useCallback(async () => {
    try {
      const result = await fetcher()
      setData(result)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err : new Error('Unknown error'))
    } finally {
      setIsLoading(false)
    }
  }, [fetcher])

  useEffect(() => {
    if (!enabled) return

    fetchData()

    const handleVisibilityChange = () => {
      if (document.visibilityState === 'visible') {
        fetchData()
        intervalRef.current = setInterval(fetchData, interval)
      } else {
        if (intervalRef.current) clearInterval(intervalRef.current)
      }
    }

    intervalRef.current = setInterval(fetchData, interval)
    document.addEventListener('visibilitychange', handleVisibilityChange)

    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current)
      document.removeEventListener('visibilitychange', handleVisibilityChange)
    }
  }, [fetchData, interval, enabled])

  return { data, isLoading, error, refetch: fetchData }
}
