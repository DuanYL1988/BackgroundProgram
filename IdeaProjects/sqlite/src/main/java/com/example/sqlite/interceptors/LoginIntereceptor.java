package com.example.sqlite.interceptors;

import com.example.sqlite.context.Context;
import com.example.sqlite.util.JWTUtil;
import org.springframework.stereotype.Component;
import org.springframework.web.servlet.HandlerInterceptor;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

@Component
public class LoginIntereceptor implements HandlerInterceptor {

    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response,Object handler) throws Exception{
        // 令牌验证
        String token = request.getHeader(Context.AUTHORIZATION);
        try {
            JWTUtil.parseToken(token);
            System.out.println(token);
            return true;
        } catch (Exception e){
            response.setStatus(401);
            return false;
        }
    }
}
