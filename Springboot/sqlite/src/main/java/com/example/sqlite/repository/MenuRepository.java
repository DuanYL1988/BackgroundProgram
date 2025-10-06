package com.example.sqlite.repository;

import java.util.List;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import com.example.sqlite.model.Menu;

@Repository
public interface MenuRepository {

    Menu selectOneById(@Param("id")Integer id);

    Menu selectOneByUniqueKey();

    int getCountByDto(Menu menu);

    List<Menu> selectByDto(Menu menu);

    int insert(Menu menu);

    int update(Menu menu);

    int delete(@Param("id")Integer id);

    List<Menu> customQuary(Menu menu);

}


