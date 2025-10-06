package com.example.mysql.repository;

import java.util.List;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.Rollback;

import com.example.mysql.dto.FireemblemHeroDto;
import com.example.mysql.model.FireemblemHero;

@SpringBootTest
class FireemblemHeroRepositoryTest {

    @Autowired
    FireemblemHeroRepository testRepository;

    @Test
    @Rollback
    public void testSample() {
        // 通过ID检索
        FireemblemHero result = testRepository.selectOneById("1");

        // 动态检索
        FireemblemHeroDto condition = new FireemblemHeroDto();
        condition.setImgName(result.getImgName());

        int searchCount = testRepository.getCountByDto(condition);
        List<FireemblemHero> resultList = testRepository.selectByDto(condition);
        // Assert.assertTrue(resultList.size() == searchCount);
        System.out.println(resultList.size() == searchCount);

        // 新ID
        String newId = result.getId() + "_N";
        // 插入
        result.setId(newId);
        testRepository.insert(result);

        // 更新
        testRepository.update(result);

        // 删除
        testRepository.delete(newId);

        // 自定义
        condition.setSelectQuary(
                "NAME AS name,RARITY AS rarity,BLESSING AS blessing,HERO_TYPE AS heroType,MOVE_TYPE AS moveType,WEAPON_TYPE AS weaponType,ENTRY AS entry,COLOR AS color,RACE AS race,SKILL_A AS skillA,SKILL_B AS skillB,SKILL_C AS skillC,HERO_RANK AS heroRank");
        condition.setCondition("");
        condition.setGroupBy("NAME,RARITY,BLESSING,HERO_TYPE,MOVE_TYPE,WEAPON_TYPE,ENTRY,COLOR,RACE,SKILL_A,SKILL_B,SKILL_C,HERO_RANK");
        condition.setHaving("count(HERO_RANK) > 1");
        condition.setOrderBy("1");
        List<FireemblemHero> custumList = testRepository.customQuary(condition);
        System.out.println(custumList.size());

    }
}
