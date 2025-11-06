package com.example.mysql.config;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;

@EnableWebSecurity
@Configuration
public class SecurityConfig extends WebSecurityConfigurerAdapter {

    // 创建BCryptPasswordEncoder注入容器
    @Bean
    public PasswordEncoder passwordEncoder(){
        return new BCryptPasswordEncoder();
    }

    @Bean
    public AuthenticationManager authenticationManager() throws  Exception {
        return super.authenticationManager();
    }

    @Autowired
    JwtAuthenticationTokenFilter tokenFilter;

    @Override
    protected void configure(HttpSecurity http) throws Exception {
        http.csrf().disable() //关闭csrf
            .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS) // 不通过Session获取SecurityContext
            .and().authorizeRequests()
                .anyRequest().permitAll(); // 所有请求都允许
                //.antMatchers("/login", "/regist").anonymous() // 放行, "/*"
                //.anyRequest().authenticated(); // 其余请求都需要验证

        http.addFilterBefore(tokenFilter, UsernamePasswordAuthenticationFilter.class);
    }
}
