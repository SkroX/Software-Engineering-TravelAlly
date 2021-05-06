package com.github.skrox.travelally.ui.auth

import android.util.Log
import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.github.skrox.travelally.data.repositories.UserRepository
import com.github.skrox.travelally.di.ActivityScope
import com.google.android.gms.auth.api.signin.GoogleSignInClient
import javax.inject.Inject

@ActivityScope
@Suppress("UNCHECKED_CAST")
class AuthViewModelFactory @Inject constructor(
    private val mGoogleSignInClient: GoogleSignInClient,
    private val repository: UserRepository
) : ViewModelProvider.NewInstanceFactory() {

    override fun <T : ViewModel?> create(modelClass: Class<T>): T {
        Log.e("authvmfact", repository.toString())
        return AuthViewModel(mGoogleSignInClient, repository) as T
    }
}