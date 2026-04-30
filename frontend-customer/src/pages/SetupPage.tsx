import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useTranslation } from 'react-i18next'
import { useAuth } from '../hooks/useAuth'
import Button from '../components/Button'

const setupSchema = z.object({
  store_code: z.string().min(1, 'auth.storeCodeRequired'),
  table_number: z.coerce.number().int().positive('auth.tableNumberRequired'),
  password: z.string().min(4, 'auth.passwordRequired'),
})

type SetupFormData = z.infer<typeof setupSchema>

export default function SetupPage() {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const { login, isAuthenticated } = useAuth()
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SetupFormData>({
    resolver: zodResolver(setupSchema),
  })

  if (isAuthenticated) {
    navigate('/', { replace: true })
    return null
  }

  const onSubmit = async (data: SetupFormData) => {
    setIsLoading(true)
    setError(null)
    try {
      await login(data)
      navigate('/', { replace: true })
    } catch {
      setError(t('auth.loginFailed'))
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-sm">
        <div className="text-center mb-8">
          <h1 className="text-2xl font-bold text-gray-900">{t('auth.setupTitle')}</h1>
        </div>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" data-testid="setup-form">
          <div>
            <label htmlFor="store_code" className="block text-sm font-medium text-gray-700 mb-1">
              {t('auth.storeCode')}
            </label>
            <input
              id="store_code"
              type="text"
              {...register('store_code')}
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              data-testid="setup-store-code"
            />
            {errors.store_code && (
              <p className="mt-1 text-sm text-red-600">{t(errors.store_code.message!)}</p>
            )}
          </div>

          <div>
            <label htmlFor="table_number" className="block text-sm font-medium text-gray-700 mb-1">
              {t('auth.tableNumber')}
            </label>
            <input
              id="table_number"
              type="number"
              inputMode="numeric"
              {...register('table_number')}
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              data-testid="setup-table-number"
            />
            {errors.table_number && (
              <p className="mt-1 text-sm text-red-600">{t(errors.table_number.message!)}</p>
            )}
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-1">
              {t('auth.password')}
            </label>
            <input
              id="password"
              type="password"
              {...register('password')}
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              data-testid="setup-password"
            />
            {errors.password && (
              <p className="mt-1 text-sm text-red-600">{t(errors.password.message!)}</p>
            )}
          </div>

          {error && (
            <div className="text-center text-sm text-red-600" role="alert">
              {error}
            </div>
          )}

          <Button
            type="submit"
            loading={isLoading}
            className="w-full"
            size="lg"
            data-testid="setup-submit"
          >
            {t('auth.submit')}
          </Button>
        </form>
      </div>
    </div>
  )
}
