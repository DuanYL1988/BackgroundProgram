package com.example.oracle.repository;

import java.util.List;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import com.example.oracle.model.Hero;

@Repository
public interface HeroRepository {

    Hero selectOneById(@Param("id")Integer id);

    Hero selectOneByUniqueKey(@Param("titleName")String titleName,@Param("name")String name);

    int getCountByDto(Hero hero);

    List<Hero> selectByDto(Hero hero);

    int insert(Hero hero);

    int update(Hero hero);

    int delete(@Param("id")Integer id);

    List<Hero> customQuary(Hero hero);

}


