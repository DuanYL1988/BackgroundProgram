package com.example.sqlite.repository;

import java.util.List;

import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import com.example.sqlite.model.Account;

@Repository
public interface AccountRepository {

    Account selectOneById(@Param("id") Integer id);

    Account selectOneByUniqueKey(@Param("loginName") String loginName);

    int getCountByDto(Account account);

    List<Account> selectByDto(Account account);

    int insert(Account account);

    int update(Account account);

    int delete(@Param("id") Integer id);

    List<Account> customQuary(Account account);

}
