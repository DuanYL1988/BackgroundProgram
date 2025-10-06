package com.example.sqlite.config;

import com.example.sqlite.interceptors.LoginIntereceptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.InterceptorRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {

    @Autowired
    private LoginIntereceptor loginIntereceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        // 登录和注册不进行验证
        registry.addInterceptor(loginIntereceptor)
            .excludePathPatterns("/login","/index","/regist");
    }
}
