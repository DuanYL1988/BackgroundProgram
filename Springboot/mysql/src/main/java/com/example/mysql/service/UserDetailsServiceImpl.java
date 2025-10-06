package com.example.mysql.service;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Objects;

import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import com.example.mysql.dto.AccountDto;
import com.example.mysql.model.Account;
import com.example.mysql.model.LoginUser;
import com.example.mysql.repository.AccountRepository;

@Service
public class UserDetailsServiceImpl implements UserDetailsService {

    private final AccountRepository accountRepository;

    public UserDetailsServiceImpl(AccountRepository accountRepository) {
        this.accountRepository = accountRepository;
    }

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        // 用户查询
        Account account;
        AccountDto condition = new AccountDto();
        try {
            if ("admin".equals(username)) {
                condition.setLoginName(username);
                account = accountRepository.selectByDto(condition).get(0);
            } else {
                // 用户名或手机号登录
                account = accountRepository.selectOneByUniqueKey(username, username, username);
            }
            //
            if (Objects.isNull(account)) {
                throw new UsernameNotFoundException("用户不存在");
            }
        } catch (Exception e) {
            throw new UsernameNotFoundException("用户不存在");
        }
        // 权限验证
        List<String> roleList = new ArrayList<>(Collections.singletonList(account.getRoleId()));

        return new LoginUser(account, roleList);
    }

}
