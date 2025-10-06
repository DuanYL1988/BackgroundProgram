package com.example.sqlite.util;

import com.auth0.jwt.JWT;
import com.auth0.jwt.JWTVerifier;
import com.auth0.jwt.algorithms.Algorithm;
import com.auth0.jwt.interfaces.Claim;
import com.auth0.jwt.interfaces.DecodedJWT;
import com.example.sqlite.context.Context;
import com.example.sqlite.model.Account;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;

public class JWTUtil {
    // 有效时间 5分钟
    private static final long limitTime = 1000 * 60 * 5;
    // 算法秘钥
    private static final String signature = "1234567890123456789012345678901234567890123";

    /**
     * 对用户信息进行jwt加密并返回token
     *
     * @param  account
     * @return
     */
    public static String createJwt(Account account) {
        return JWT.create()
                .withClaim(Context.USER_ID, account.getId()+"")
                .withClaim(Context.USER_NAME, account.getUsername())
                .withClaim(Context.USER_APP, account.getApplication())
                .withClaim(Context.USER_ROLE, account.getGroupName())
                .withClaim(Context.USER_COMPANY, account.getCompany())
                .withExpiresAt(new Date(System.currentTimeMillis() + limitTime))
                .sign(Algorithm.HMAC256(signature));
    }

    /**
     * 解密token并返回json信息的Map
     *
     * @param  token
     * @return
     */
    public static Map<String, String> parseToken(String token) {
        JWTVerifier jwtVerifier = JWT.require(Algorithm.HMAC256(signature)).build();
        DecodedJWT decodedJWT = jwtVerifier.verify(token);
        Map<String, Claim> claims = decodedJWT.getClaims();
        Map<String, String> result = new HashMap<String, String>();
        for(String key : claims.keySet()) {
            result.put(key, claims.get(key).asString());
        }
        return result;
    }
}
