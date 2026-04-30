import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useTranslation } from 'react-i18next'
import { loginAdmin } from '../api/auth'
import { useAdminAuthStore } from '../store/authStore'
import { ApiError } from '../api/client'

const loginSchema = z.object({
  store_code: z.string().min(1, 'required'),
  username: z.string().min(1, 'required'),
  password: z.string().min(1, 'required'),
})

type LoginFormData = z.infer<typeof loginSchema>

export default function LoginPage() {
  const { t } = useTranslation()
  const navigate = useNavigate()
  const adminLogin = useAdminAuthStore((s) => s.login)
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({ resolver: zodResolver(loginSchema) })

  const onSubmit = async (data: LoginFormData) => {
    setIsLoading(true)
    setError(null)
    try {
      const response = await loginAdmin(data)
      adminLogin({
        token: response.token,
        role: response.role,
        storeId: response.store_id,
        username: response.username,
      })
      navigate('/', { replace: true })
    } catch (err) {
      if (err instanceof ApiError && err.statusCode === 429) {
        setError(t('auth.lockedOut', { minutes: 15 }))
      } else {
        setError(t('auth.loginFailed'))
      }
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="w-full max-w-sm bg-white rounded-2xl shadow-sm p-8">
        <h1 className="text-2xl font-bold text-center text-gray-900 mb-6">{t('auth.loginTitle')}</h1>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" data-testid="login-form">
          <div>
            <label htmlFor="store_code" className="block text-sm font-medium text-gray-700 mb-1">
              {t('auth.storeCode')}
            </label>
            <input
              id="store_code"
              type="text"
              {...register('store_code')}
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              data-testid="login-store-code"
            />
            {errors.store_code && <p className="mt-1 text-sm text-red-600">{t('auth.storeCode')}을 입력해주세요</p>}
          </div>

          <div>
            <label htmlFor="username" className="block text-sm font-medium text-gray-700 mb-1">
              {t('auth.username')}
            </label>
            <input
              id="username"
              type="text"
              {...register('username')}
              className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              data-testid="login-username"
            />
            {errors.username && <p className="mt-1 text-sm text-red-600">{t('auth.username')}을 입력해주세요</p>}
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
              data-testid="login-password"
            />
          </div>

          {error && <div className="text-center text-sm text-red-600" role="alert">{error}</div>}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3 bg-primary-600 text-white font-medium rounded-xl hover:bg-primary-700 disabled:bg-gray-300 transition-colors"
            data-testid="login-submit"
          >
            {isLoading ? t('common.loading') : t('auth.login')}
          </button>
        </form>
      </div>
    </div>
  )
}
