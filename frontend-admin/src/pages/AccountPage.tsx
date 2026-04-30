import { useState } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { useTranslation } from 'react-i18next'
import { registerAccount } from '../api/auth'
import { ApiError } from '../api/client'

const accountSchema = z
  .object({
    username: z.string().min(3, 'account.usernameRule').max(50).regex(/^[a-zA-Z0-9]+$/, 'account.usernameRule'),
    password: z.string().min(4, 'table.passwordMin'),
    passwordConfirm: z.string().min(1),
  })
  .refine((data) => data.password === data.passwordConfirm, {
    message: 'account.passwordMismatch',
    path: ['passwordConfirm'],
  })

type AccountFormData = z.infer<typeof accountSchema>

export default function AccountPage() {
  const { t } = useTranslation()
  const [success, setSuccess] = useState<string | null>(null)
  const [error, setError] = useState<string | null>(null)
  const [isLoading, setIsLoading] = useState(false)

  const { register, handleSubmit, reset, formState: { errors } } = useForm<AccountFormData>({
    resolver: zodResolver(accountSchema),
  })

  const onSubmit = async (data: AccountFormData) => {
    setIsLoading(true)
    setError(null)
    setSuccess(null)
    try {
      await registerAccount({ username: data.username, password: data.password })
      setSuccess(t('account.registerSuccess'))
      reset()
    } catch (err) {
      if (err instanceof ApiError && err.statusCode === 409) {
        setError(t('account.duplicateError'))
      } else {
        setError(t('common.error'))
      }
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div>
      <h2 className="text-xl font-bold text-gray-900 mb-6">{t('account.title')}</h2>

      <div className="bg-white rounded-xl p-6 max-w-md">
        <h3 className="text-lg font-semibold mb-4">{t('account.register')}</h3>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4" data-testid="account-form">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">{t('account.username')} *</label>
            <input {...register('username')} className="w-full px-4 py-2.5 border border-gray-300 rounded-xl" data-testid="account-username" />
            {errors.username && <p className="mt-1 text-sm text-red-600">{t(errors.username.message!)}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">{t('account.password')} *</label>
            <input type="password" {...register('password')} className="w-full px-4 py-2.5 border border-gray-300 rounded-xl" data-testid="account-password" />
            {errors.password && <p className="mt-1 text-sm text-red-600">{t(errors.password.message!)}</p>}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">{t('account.passwordConfirm')} *</label>
            <input type="password" {...register('passwordConfirm')} className="w-full px-4 py-2.5 border border-gray-300 rounded-xl" data-testid="account-password-confirm" />
            {errors.passwordConfirm && <p className="mt-1 text-sm text-red-600">{t(errors.passwordConfirm.message!)}</p>}
          </div>

          {success && <div className="text-sm text-green-600 text-center" role="status">{success}</div>}
          {error && <div className="text-sm text-red-600 text-center" role="alert">{error}</div>}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-2.5 bg-primary-600 text-white rounded-xl hover:bg-primary-700 disabled:bg-gray-300 font-medium"
            data-testid="account-submit"
          >
            {isLoading ? t('common.loading') : t('account.register')}
          </button>
        </form>
      </div>
    </div>
  )
}
