import { useTranslation } from 'react-i18next'
import Button from './Button'

interface ErrorMessageProps {
  message: string
  onRetry?: () => void
}

export default function ErrorMessage({ message, onRetry }: ErrorMessageProps) {
  const { t } = useTranslation()
  return (
    <div className="flex flex-col items-center justify-center py-8 text-center" role="alert">
      <p className="text-red-600 font-medium">{message}</p>
      {onRetry && (
        <Button variant="secondary" size="sm" className="mt-3" onClick={onRetry}>
          {t('common.retry')}
        </Button>
      )}
    </div>
  )
}
