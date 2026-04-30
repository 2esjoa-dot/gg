-- 태국 음식점 메뉴 시드 데이터 SQL
-- 사용법: psql -d table_order_dev -f scripts/seed_thai_menu.sql

BEGIN;

-- 1. 매장 생성 (이미 존재하면 스킵)
INSERT INTO stores (name, code, address, is_active)
VALUES ('태국 음식점', 'thai-restaurant', '서울시 강남구', true)
ON CONFLICT (code) DO NOTHING;

-- store_id 변수 설정
DO $$
DECLARE
    v_store_id INT;
    v_cat_main INT;
    v_cat_side INT;
    v_cat_drink INT;
    v_cat_set INT;
BEGIN
    SELECT id INTO v_store_id FROM stores WHERE code = 'thai-restaurant';

    -- 2. 카테고리 생성
    INSERT INTO categories (store_id, name, display_order)
    VALUES (v_store_id, '대표 메뉴', 1)
    ON CONFLICT ON CONSTRAINT uq_category_store_name DO UPDATE SET display_order = 1
    RETURNING id INTO v_cat_main;

    INSERT INTO categories (store_id, name, display_order)
    VALUES (v_store_id, '추가 메뉴', 2)
    ON CONFLICT ON CONSTRAINT uq_category_store_name DO UPDATE SET display_order = 2
    RETURNING id INTO v_cat_side;

    INSERT INTO categories (store_id, name, display_order)
    VALUES (v_store_id, '음료', 3)
    ON CONFLICT ON CONSTRAINT uq_category_store_name DO UPDATE SET display_order = 3
    RETURNING id INTO v_cat_drink;

    INSERT INTO categories (store_id, name, display_order)
    VALUES (v_store_id, '세트 메뉴', 4)
    ON CONFLICT ON CONSTRAINT uq_category_store_name DO UPDATE SET display_order = 4
    RETURNING id INTO v_cat_set;

    -- 3. 대표 메뉴
    INSERT INTO menu_items (store_id, category_id, name, price, description, display_order, is_active)
    VALUES
        (v_store_id, v_cat_main, '팟타이 꿍', 13000, '태국식 볶음 쌀국수 (새우) | 알레르기: 새우, 땅콩, 달걀', 1, true),
        (v_store_id, v_cat_main, '푸팟퐁커리 (라이스 포함)', 28000, '부드러운 소프트쉘 크랩 커리 | 알레르기: 게, 달걀, 우유, 대두', 2, true),
        (v_store_id, v_cat_main, '카오팟 사파롯', 14000, '파인애플 새우 볶음밥 | 알레르기: 새우, 캐슈넛, 달걀', 3, true),
        (v_store_id, v_cat_main, '꾸웨이띠여우 느어', 12000, '진한 육수의 태국식 소고기 쌀국수 | 알레르기: 쇠고기, 대두', 4, true),
        (v_store_id, v_cat_main, '똠양꿍 (면/밥 선택)', 16000, '세계 3대 스프로 꼽히는 새콤매콤한 탕 | 알레르기: 새우, 우유, 버섯', 5, true)
    ON CONFLICT DO NOTHING;

    -- 4. 추가 메뉴
    INSERT INTO menu_items (store_id, category_id, name, price, description, display_order, is_active)
    VALUES
        (v_store_id, v_cat_side, '텃만꿍 (4pcs)', 10000, '다진 새우 살을 튀겨낸 도넛 모양 고로케 | 알레르기: 새우, 밀, 달걀', 1, true),
        (v_store_id, v_cat_side, '뽀삐아 톳 (4pcs)', 8000, '채소와 당면을 넣어 튀긴 태국식 춘권 | 알레르기: 밀, 대두', 2, true),
        (v_store_id, v_cat_side, '쏨땀 타이', 11000, '그린 파파야로 만든 매콤새콤한 샐러드 | 알레르기: 땅콩, 피쉬소스(어류), 마른새우', 3, true),
        (v_store_id, v_cat_side, '공공치킨 (까이텃)', 9000, '태국식 시즈닝으로 튀긴 닭날개 요리 | 알레르기: 닭고기, 밀', 4, true)
    ON CONFLICT DO NOTHING;

    -- 5. 음료
    INSERT INTO menu_items (store_id, category_id, name, price, description, display_order, is_active)
    VALUES
        (v_store_id, v_cat_drink, '타이 밀크티', 5500, '연유가 들어간 달콤하고 진한 태국 홍차 | 알레르기: 우유', 1, true),
        (v_store_id, v_cat_drink, '땡모반', 6500, '여름 시즌 한정 시원한 수박 생과일 주스', 2, true),
        (v_store_id, v_cat_drink, '창(Chang) / 싱하(Singha)', 7000, '태국 대표 병맥주 | 알코올 포함', 3, true),
        (v_store_id, v_cat_drink, '망고 에이드', 5000, '달콤한 망고 과육이 씹히는 에이드', 4, true)
    ON CONFLICT DO NOTHING;

    -- 6. 세트 메뉴
    INSERT INTO menu_items (store_id, category_id, name, price, description, display_order, is_active)
    VALUES
        (v_store_id, v_cat_set, '2인 실속 세트', 40000, '팟타이 꿍 + 카오팟 사파롯 + 텃만꿍(2pcs) + 에이드 1잔', 1, true),
        (v_store_id, v_cat_set, '시그니처 커리 세트', 52000, '푸팟퐁커리 + 팟타이 꿍 + 쏨땀 타이 + 공기밥 1개', 2, true),
        (v_store_id, v_cat_set, '혼밥 1인 세트', 18000, '소고기 쌀국수(S) + 뽀삐아 톳(2pcs) + 타이 밀크티', 3, true)
    ON CONFLICT DO NOTHING;

    RAISE NOTICE '✅ 시드 완료: store_id=%, 대표메뉴=5, 추가메뉴=4, 음료=4, 세트=3', v_store_id;
END $$;

COMMIT;
