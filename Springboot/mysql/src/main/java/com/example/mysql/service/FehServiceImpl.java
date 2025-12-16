package com.example.mysql.service;

import com.example.mysql.dto.FireemblemHeroDto;
import com.example.mysql.model.FireemblemHero;
import com.example.mysql.repository.CustomizeRepository;
import com.example.mysql.repository.FireemblemHeroRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class FehServiceImpl {

    @Autowired
    FireemblemHeroRepository fehDao;

    @Autowired
    CustomizeRepository testDao;

    public Map<String, Object> getHerosInfo(FireemblemHeroDto dto){
        // 根据条件取得情报
        List<FireemblemHero> heroList = fehDao.selectByDto(dto);

        // 取得关联技能情报
        List<Map<String, Object>> dbResult = testDao.getFehSkillsInfo(dto);

        // 技能分组
        Map<String,Object> skillDirt = new HashMap<>();
        for (Map<String, Object> row : dbResult) {
            skillDirt.put((String)row.get("imgName"), row);
        }

        // 处理结果
        Map<String, Object> result = new HashMap<>();
        result.put("skillDirt",skillDirt);
        result.put("dataList",heroList);
        return result;
    }

}
