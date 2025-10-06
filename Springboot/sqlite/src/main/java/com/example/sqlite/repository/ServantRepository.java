package com.example.sqlite.repository;

import java.util.List;
import org.apache.ibatis.annotations.Param;
import org.springframework.stereotype.Repository;

import com.example.sqlite.model.Servant;

@Repository
public interface ServantRepository {

    Servant selectOneById(@Param("id")String id);

    Servant selectOneByUniqueKey(@Param("imgName")String imgName);

    int getCountByDto(Servant servant);

    List<Servant> selectByDto(Servant servant);

    int insert(Servant servant);

    int update(Servant servant);

    int delete(@Param("id")String id);

    List<Servant> customQuary(Servant servant);

}


