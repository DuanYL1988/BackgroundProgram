package com.example.mysql.config;

import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Objects;

import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;
import org.springframework.web.filter.OncePerRequestFilter;

import com.example.mysql.model.Account;
import com.example.mysql.model.LoginUser;
import com.example.mysql.repository.AccountRepository;
import com.example.mysql.util.JWTUtil;

@Component
public class JwtAuthenticationTokenFilter extends OncePerRequestFilter {

    private final AccountRepository accountRepository;

    public JwtAuthenticationTokenFilter(AccountRepository accountRepository) {
        this.accountRepository = accountRepository;
    }

    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, FilterChain filterChain) throws ServletException, IOException {
        // 获取token
        String token = request.getHeader("Authorization");
        if (!StringUtils.hasText(token)) {
            filterChain.doFilter(request, response);
            return;
        }
        // 解析token
        Map<String, String> result = JWTUtil.parseToken(token);
        Account account = accountRepository.selectOneById(result.get("id"));
        if (Objects.isNull(account)) {
            throw new RuntimeException("用户被删除");
        }
        // 存入SecurityContextHolder
        List<String> roleList = new ArrayList<>(Collections.singletonList(account.getRoleId()));
        LoginUser user = new LoginUser(account, roleList);
        UsernamePasswordAuthenticationToken usernamePasswordAuthenticationToken = new UsernamePasswordAuthenticationToken(user, null, null);
        SecurityContextHolder.getContext().setAuthentication(usernamePasswordAuthenticationToken);
        // 放行
        filterChain.doFilter(request, response);
    }
}
