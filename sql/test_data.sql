-- Заполнение таблицы users (с статическим id)
INSERT INTO users (id, username, email, password, is_active, is_admin, created_at, updated_at, created_by, updated_by)
VALUES
(1, 'user1', 'user1@test.com', 'hashed_password_1', TRUE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL),
(2, 'user2', 'user2@test.com', 'hashed_password_2', TRUE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL),
(3, 'user3', 'user3@test.com', 'hashed_password_3', FALSE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL),
(4, 'user11', 'user11@test.com', 'hashed_password_11', TRUE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL),
(5, 'user12', 'user12@test.com', 'hashed_password_12', TRUE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL),
(6, 'user13', 'user13@test.com', 'hashed_password_13', FALSE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL),
(7, 'user14', 'user14@test.com', 'hashed_password_14', TRUE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL),
(8, 'user15', 'user15@test.com', 'hashed_password_15', TRUE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL),
(9, 'user16', 'user16@test.com', 'hashed_password_16', FALSE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL),
(10, 'user17', 'user17@test.com', 'hashed_password_17', TRUE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL),
(11, 'user18', 'user18@test.com', 'hashed_password_18', TRUE, TRUE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL),
(12, 'user19', 'user19@test.com', 'hashed_password_19', FALSE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL),
(13, 'user20', 'user20@test.com', 'hashed_password_20', TRUE, FALSE, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL);
-- Set the last value for the users table
ALTER SEQUENCE users_id_seq RESTART WITH 14;  -- Next ID will be 14



-- Заполнение таблицы categories (с статическим id)
INSERT INTO categories (id, name, description, created_at, updated_at, created_by, updated_by, is_active)
VALUES
(1, 'Coffee', 'Different types of coffee drinks', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(2, 'Tea', 'Variety of teas', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(3, 'Pastries', 'Baked goods and sweets', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(4, 'Sandwiches', 'Light meals and snacks', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(5, 'Desserts', 'Sweet treats', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(6, 'Milkshakes', 'Cold blended drinks', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(7, 'Smoothies', 'Fruit and vegetable blends', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(8, 'Snacks', 'Quick bites', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(9, 'Hot Drinks', 'Other hot beverages', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(10, 'Cold Drinks', 'Refreshing cold beverages', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE);

-- Set the last value for the categories table
ALTER SEQUENCE categories_id_seq RESTART WITH 11;  -- Next ID will be 11

-- Заполнение таблицы products (с статическим id)
INSERT INTO products (id, name, description, price, image_url, category_id, created_at, updated_at, created_by, updated_by, is_active)
VALUES
(1, 'Espresso', 'Strong black coffee', 2.50, 'http://example.com/espresso.jpg', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(2, 'Latte', 'Coffee with steamed milk', 3.50, 'http://example.com/latte.jpg', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(3, 'Green Tea', 'Classic green tea', 2.00, 'http://example.com/greentea.jpg', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(4, 'Croissant', 'Buttery pastry', 2.80, 'http://example.com/croissant.jpg', 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(5, 'Turkey Sandwich', 'Turkey and cheese sandwich', 5.50, 'http://example.com/turkeysandwich.jpg', 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(6, 'Americano', 'Hot coffee with water', 3.00, 'http://example.com/americano.jpg', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(7, 'Cappuccino', 'Espresso with foamed milk', 4.00, 'http://example.com/cappuccino.jpg', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(8, 'Black Tea', 'Simple black tea leaves', 2.20, 'http://example.com/blacktea.jpg', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(9, 'Herbal Tea', 'Caffeine-free herbal infusion', 2.50, 'http://example.com/herbaltea.jpg', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(10, 'Muffin', 'Chocolate chip muffin', 3.20, 'http://example.com/muffin.jpg', 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(11, 'Donut', 'Glazed donut', 2.00, 'http://example.com/donut.jpg', 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(12, 'Veggie Sandwich', 'Vegetable and hummus sandwich', 6.00, 'http://example.com/veggiesandwich.jpg', 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(13, 'Club Sandwich', 'Chicken club sandwich', 7.50, 'http://example.com/clubsandwich.jpg', 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(14, 'Cheesecake', 'Creamy cheesecake dessert', 5.00, 'http://example.com/cheesecake.jpg', 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(15, 'Ice Cream', 'Vanilla ice cream scoop', 4.50, 'http://example.com/icecream.jpg', 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(16, 'Chocolate Milkshake', 'Rich chocolate shake', 5.50, 'http://example.com/chocolatemilkshake.jpg', 6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(17, 'Strawberry Milkshake', 'Fresh strawberry blend', 5.50, 'http://example.com/strawberrymilkshake.jpg', 6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(18, 'Berry Smoothie', 'Mixed berry smoothie', 4.00, 'http://example.com/berrysmoothie.jpg', 7, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(19, 'Green Smoothie', 'Spinach and fruit smoothie', 4.50, 'http://example.com/greensmoothie.jpg', 7, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(20, 'Popcorn', 'Salted popcorn snack', 2.50, 'http://example.com/popcorn.jpg', 8, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(21, 'Nuts Mix', 'Assorted nuts', 3.00, 'http://example.com/nuts.jpg', 8, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(22, 'Hot Chocolate', 'Warm chocolate drink', 3.50, 'http://example.com/hotchocolate.jpg', 9, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(23, 'Spiced Cider', 'Apple cider with spices', 3.00, 'http://example.com/spicedcider.jpg', 9, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(24, 'Lemonade', 'Fresh lemonade', 2.50, 'http://example.com/lemonade.jpg', 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(25, 'Iced Tea', 'Chilled tea with lemon', 2.80, 'http://example.com/icedtea.jpg', 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(26, 'Mocha', 'Espresso with chocolate and milk', 4.50, 'http://example.com/mocha.jpg', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(27, 'Flat White', 'Espresso with steamed milk', 3.80, 'http://example.com/flatwhite.jpg', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(28, 'Oolong Tea', 'Semi-fermented tea with floral notes', 2.70, 'http://example.com/oolongtea.jpg', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(29, 'Chamomile Tea', 'Herbal tea for relaxation', 2.40, 'http://example.com/chamomiletea.jpg', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(30, 'Bagel', 'Toasted bagel with seeds', 2.90, 'http://example.com/bagel.jpg', 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(31, 'Éclair', 'Pastry filled with cream', 3.50, 'http://example.com/eclair.jpg', 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(32, 'BLT Sandwich', 'Bacon, lettuce, and tomato sandwich', 6.50, 'http://example.com/bltsandwich.jpg', 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(33, 'Grilled Cheese', 'Melted cheese on toasted bread', 5.00, 'http://example.com/grilledcheese.jpg', 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(34, 'Tiramisu', 'Coffee-flavored Italian dessert', 6.00, 'http://example.com/tiramisu.jpg', 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(35, 'Brownie', 'Fudgy chocolate brownie', 4.00, 'http://example.com/brownie.jpg', 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(36, 'Banana Milkshake', 'Milkshake with fresh bananas', 5.00, 'http://example.com/bananamilkshake.jpg', 6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(37, 'Oreo Milkshake', 'Milkshake with Oreo cookies', 5.50, 'http://example.com/oreomilkshake.jpg', 6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(38, 'Mango Smoothie', 'Tropical mango and yogurt blend', 4.20, 'http://example.com/mangosmoothie.jpg', 7, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(39, 'Kale Smoothie', 'Healthy kale and fruit mix', 4.80, 'http://example.com/kalesmoothie.jpg', 7, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(40, 'Pretzels', 'Salted soft pretzels', 3.20, 'http://example.com/pretzels.jpg', 8, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(41, 'Trail Mix', 'Mix of nuts and dried fruits', 3.50, 'http://example.com/trailmix.jpg', 8, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(42, 'Chai Latte', 'Spiced tea with milk', 4.20, 'http://example.com/chailatte.jpg', 9, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(43, 'Mocha Latte', 'Coffee latte with chocolate', 4.70, 'http://example.com/mochalatte.jpg', 9, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(44, 'Sparkling Water', 'Carbonated flavored water', 2.00, 'http://example.com/sparklingwater.jpg', 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(45, 'Fruit Punch', 'Refreshing mixed fruit drink', 3.00, 'http://example.com/fruitpunch.jpg', 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(46, 'Caramel Macchiato', 'Espresso with caramel syrup and milk', 4.20, 'http://example.com/caramelmacchiato.jpg', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(47, 'Iced Coffee', 'Chilled coffee with ice', 3.00, 'http://example.com/icedcoffee.jpg', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(48, 'White Tea', 'Delicate white tea leaves', 2.60, 'http://example.com/whitetea.jpg', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(49, 'Earl Grey Tea', 'Black tea with bergamot', 2.30, 'http://example.com/earlgrey.jpg', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(50, 'Danish Pastry', 'Flaky pastry with fruit filling', 3.40, 'http://example.com/danishpastry.jpg', 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(51, 'Cinnamon Roll', 'Sweet roll with cinnamon', 3.00, 'http://example.com/cinnamonroll.jpg', 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(52, 'Vegan Sandwich', 'Plant-based sandwich with veggies', 6.20, 'http://example.com/vegansandwich.jpg', 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(53, 'Ham Sandwich', 'Ham and cheese on bread', 5.80, 'http://example.com/hamsandwich.jpg', 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(54, 'Panna Cotta', 'Italian cream dessert', 5.50, 'http://example.com/pannacotta.jpg', 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(55, 'Fruit Tart', 'Tart with fresh fruits', 4.80, 'http://example.com/fruittart.jpg', 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(56, 'Vanilla Milkshake', 'Classic vanilla shake', 5.00, 'http://example.com/vanillamilkshake.jpg', 6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(57, 'Cookies and Cream Shake', 'Milkshake with cookies', 5.60, 'http://example.com/cookiesandcream.jpg', 6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(58, 'Pineapple Smoothie', 'Tropical pineapple blend', 4.30, 'http://example.com/pineapplesmoothie.jpg', 7, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(59, 'Avocado Smoothie', 'Creamy avocado mix', 4.90, 'http://example.com/avocadosmoothie.jpg', 7, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(60, 'Cheese Puffs', 'Cheesy baked puffs', 2.70, 'http://example.com/cheesepuffs.jpg', 8, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(61, 'Granola Bar', 'Healthy snack bar', 2.90, 'http://example.com/granola.jpg', 8, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(62, 'Ginger Tea', 'Spicy ginger infusion', 3.10, 'http://example.com/gingertea.jpg', 9, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(63, 'Turmeric Latte', 'Golden milk with turmeric', 4.00, 'http://example.com/turmericlatte.jpg', 9, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(64, 'Coconut Water', 'Natural coconut refreshment', 2.50, 'http://example.com/coconutwater.jpg', 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(65, 'Orange Juice', 'Fresh squeezed orange juice', 3.20, 'http://example.com/orangejuice.jpg', 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(66, 'Affogato', 'Espresso over ice cream', 4.50, 'http://example.com/affogato.jpg', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(67, 'Cold Brew', 'Smooth cold-brewed coffee', 3.50, 'http://example.com/coldbrew.jpg', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(68, 'Rooibos Tea', 'Caffeine-free red tea', 2.40, 'http://example.com/rooibostea.jpg', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(69, 'Peppermint Tea', 'Refreshing mint tea', 2.20, 'http://example.com/pepperminttea.jpg', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(70, 'Apple Strudel', 'Pastry with apples', 3.60, 'http://example.com/applestrudel.jpg', 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(71, 'Scone', 'British-style baked good', 2.80, 'http://example.com/scone.jpg', 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(72, 'Egg Sandwich', 'Breakfast egg sandwich', 6.00, 'http://example.com/eggsandwich.jpg', 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(73, 'Caprese Sandwich', 'Tomato, mozzarella, basil', 6.50, 'http://example.com/capresesandwich.jpg', 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(74, 'Key Lime Pie', 'Tart lime dessert', 5.20, 'http://example.com/keylimepie.jpg', 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(75, 'Macaron', 'French almond cookie', 4.00, 'http://example.com/macaron.jpg', 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(76, 'Peanut Butter Shake', 'Nutty milkshake', 5.30, 'http://example.com/peanutbuttershake.jpg', 6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(77, 'Blueberry Shake', 'Berry-infused shake', 5.40, 'http://example.com/blueberryshake.jpg', 6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(78, 'Watermelon Smoothie', 'Refreshing summer drink', 4.10, 'http://example.com/watermelonsmoothie.jpg', 7, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(79, 'Beet Smoothie', 'Nutritious beet blend', 4.70, 'http://example.com/beetsmoothie.jpg', 7, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(80, 'Yogurt Parfait', 'Layered yogurt snack', 3.00, 'http://example.com/yogurtparfait.jpg', 8, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(81, 'Energy Bar', 'High-energy snack', 3.10, 'http://example.com/energybar.jpg', 8, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(82, 'Elderflower Tea', 'Floral herbal tea', 3.30, 'http://example.com/elderflowertea.jpg', 9, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(83, 'Matcha Latte', 'Green tea latte', 4.10, 'http://example.com/matchalatte.jpg', 9, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(84, 'Aloe Vera Drink', 'Soothing aloe drink', 2.60, 'http://example.com/aloeveradrink.jpg', 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(85, 'Grapefruit Soda', 'Fizzy grapefruit drink', 2.80, 'http://example.com/grapefruitsoda.jpg', 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(86, 'Nitro Coffee', 'Nitrogen-infused coffee', 4.00, 'http://example.com/nitrocoffee.jpg', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(87, 'Doppio', 'Double shot espresso', 3.20, 'http://example.com/doppio.jpg', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(88, 'Jasmine Tea', 'Fragrant jasmine-infused tea', 2.50, 'http://example.com/jasminetea.jpg', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(89, 'Hibiscus Tea', 'Tart hibiscus brew', 2.40, 'http://example.com/hibiscustea.jpg', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(90, 'Brioche', 'Soft French bread', 3.00, 'http://example.com/brioche.jpg', 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(91, 'Bear Claw', 'Pastry with almond filling', 3.50, 'http://example.com/bearclaw.jpg', 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(92, 'Tuna Salad Sandwich', 'Fresh tuna on bread', 6.40, 'http://example.com/tunasandwich.jpg', 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(93, 'Philly Cheesesteak', 'Steak and cheese sandwich', 7.00, 'http://example.com/phillycheesesteak.jpg', 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(94, 'Crème Brûlée', 'Crispy-topped custard', 5.60, 'http://example.com/cremebrulee.jpg', 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(95, 'Chocolate Mousse', 'Light chocolate dessert', 4.50, 'http://example.com/chocolatemousse.jpg', 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(96, 'Coffee Shake', 'Coffee-flavored milkshake', 5.20, 'http://example.com/coffeeshake.jpg', 6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(97, 'Mango Lassi', 'Yogurt-based shake', 5.00, 'http://example.com/mangolassi.jpg', 6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(98, 'Kiwi Smoothie', 'Fresh kiwi blend', 4.40, 'http://example.com/kiwismoothie.jpg', 7, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(99, 'Spinach Banana Smoothie', 'Green energy boost', 4.60, 'http://example.com/spinachbananasmoothie.jpg', 7, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(100, 'Veggie Chips', 'Baked vegetable chips', 2.90, 'http://example.com/veggiechips.jpg', 8, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(101, 'Protein Bar', 'Nutritious protein snack', 3.20, 'http://example.com/proteinbar.jpg', 8, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(102, 'Lemon Ginger Tea', 'Zesty ginger tea', 3.40, 'http://example.com/lemongingertea.jpg', 9, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(103, 'Cocoa', 'Hot chocolate drink', 3.50, 'http://example.com/cocoa.jpg', 9, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(104, 'Mint Infused Water', 'Refreshing mint water', 2.30, 'http://example.com/mintwater.jpg', 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(105, 'Berry Infused Water', 'Fruit-flavored water', 2.40, 'http://example.com/berrywater.jpg', 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(106, 'Vienna Coffee', 'Whipped cream coffee', 4.30, 'http://example.com/viennacoffee.jpg', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(107, 'Ristretto', 'Short, intense espresso', 3.10, 'http://example.com/ristretto.jpg', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(108, 'Darjeeling Tea', 'Fine black tea', 2.70, 'http://example.com/darjeelingtea.jpg', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(109, 'Lavender Tea', 'Calming lavender brew', 2.50, 'http://example.com/lavendertea.jpg', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(110, 'Focaccia', 'Italian flatbread', 3.20, 'http://example.com/focaccia.jpg', 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(111, 'Pain au Chocolat', 'Chocolate-filled croissant', 3.40, 'http://example.com/painauchocolat.jpg', 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(112, 'Falafel Wrap', 'Middle Eastern wrap', 6.50, 'http://example.com/falafelwrap.jpg', 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(113, 'Avocado Toast Sandwich', 'Trendy avocado on toast', 5.90, 'http://example.com/avocadotoast.jpg', 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(114, 'Lemon Tart', 'Zesty lemon dessert', 5.00, 'http://example.com/lemontart.jpg', 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(115, 'Pudding', 'Classic vanilla pudding', 4.20, 'http://example.com/pudding.jpg', 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(116, 'Almond Milk Shake', 'Dairy-free shake', 5.10, 'http://example.com/almondmilkshake.jpg', 6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(117, 'Hazelnut Shake', 'Nutty flavor shake', 5.30, 'http://example.com/hazelnutshake.jpg', 6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(118, 'Cucumber Smoothie', 'Cooling cucumber blend', 4.20, 'http://example.com/cucumbersmoothie.jpg', 7, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(119, 'Carrot Ginger Smoothie', 'Spicy carrot mix', 4.80, 'http://example.com/carrotgingersmoothie.jpg', 7, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(120, 'Hummus with Veggies', 'Dip and crudites', 3.00, 'http://example.com/hummus.jpg', 8, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(121, 'Dried Fruit Mix', 'Assorted dried fruits', 3.30, 'http://example.com/driedfruit.jpg', 8, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(122, 'Rosehip Tea', 'Vitamin-rich tea', 3.00, 'http://example.com/rosehiptea.jpg', 9, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(123, 'Cardamom Coffee', 'Spiced coffee brew', 4.40, 'http://example.com/cardamomcoffee.jpg', 9, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(124, 'Hibiscus Cooler', 'Iced hibiscus drink', 2.70, 'http://example.com/hibiscuscooler.jpg', 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(125, 'Limeade', 'Lime-flavored drink', 2.90, 'http://example.com/limeade.jpg', 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(126, 'Espresso Tonic', 'Espresso with tonic water', 4.10, 'http://example.com/espressotonic.jpg', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(127, 'Flat White Variation', 'Creamy espresso drink', 3.90, 'http://example.com/flatwhitevariation.jpg', 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(128, 'Assam Tea', 'Robust black tea', 2.80, 'http://example.com/assamtea.jpg', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(129, 'Mint Chamomile', 'Mint and chamomile blend', 2.60, 'http://example.com/mintchamomile.jpg', 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(130, 'Zucchini Bread', 'Moist baked bread', 3.50, 'http://example.com/zucchinibread.jpg', 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(131, 'Poppy Seed Muffin', 'Muffin with poppy seeds', 3.10, 'http://example.com/poppyseedmuffin.jpg', 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(132, 'Greek Salad Wrap', 'Fresh salad in a wrap', 6.70, 'http://example.com/greeksaladwrap.jpg', 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(133, 'Chicken Caesar Wrap', 'Classic Caesar in a wrap', 7.20, 'http://example.com/chickencaesarwrap.jpg', 4, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(134, 'Raspberry Sorbet', 'Frozen raspberry treat', 4.90, 'http://example.com/raspberrysorbet.jpg', 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(135, 'Custard Tart', 'Egg-based tart', 5.10, 'http://example.com/custardtart.jpg', 5, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(136, 'Espresso Shake', 'Coffee and milk blend', 5.40, 'http://example.com/espressoshake.jpg', 6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(137, 'Strawberry Banana Shake', 'Fruit mix shake', 5.20, 'http://example.com/strawberrybananashake.jpg', 6, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(138, 'Peach Smoothie', 'Sweet peach blend', 4.50, 'http://example.com/peachsmoothie.jpg', 7, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(139, 'Apple Cinnamon Smoothie', 'Spiced apple drink', 4.60, 'http://example.com/applecinnamonsmoothie.jpg', 7, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(140, 'Guacamole', 'Avocado dip with chips', 3.40, 'http://example.com/guacamole.jpg', 8, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(141, 'Nut Butter', 'Spreadable nut mix', 3.50, 'http://example.com/nutbutter.jpg', 8, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(142, 'Fennel Tea', 'Digestive fennel brew', 3.20, 'http://example.com/fenneltea.jpg', 9, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(143, 'Anise Coffee', 'Licorice-flavored coffee', 4.30, 'http://example.com/anisecoffee.jpg', 9, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(144, 'Cucumber Lime Water', 'Hydrating infused water', 2.40, 'http://example.com/cucumberlimewater.jpg', 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(145, 'Kiwi Cooler', 'Kiwi and lime drink', 2.60, 'http://example.com/kiwicooler.jpg', 10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE);

-- Set the last value for the products table
ALTER SEQUENCE products_id_seq RESTART WITH 146;  -- Next ID will be 146


-- Заполнение таблицы carts (с статическим id)
INSERT INTO carts (id, user_id, created_at, updated_at, created_by, updated_by, is_active)
VALUES
(1, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(2, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(3, 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE);
-- Set the last value for the carts table
ALTER SEQUENCE carts_id_seq RESTART WITH 4;  -- Next ID will be 4


-- Заполнение таблицы cart_products (с статическим id)
INSERT INTO cart_products (id, cart_id, product_id, quantity, created_at, updated_at, created_by, updated_by, is_active)
VALUES
(1, 1, 1, 2, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(2, 1, 2, 1, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(3, 2, 3, 3, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE);

ALTER SEQUENCE cart_products_id_seq RESTART WITH 4;  -- Next ID will be 4

-- Заполнение таблицы orders (с статическим id)
INSERT INTO orders (id, user_id, status, total_amount, created_at, updated_at, created_by, updated_by, is_active)
VALUES
(1, 1, 'PENDING', 8.50, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(2, 2, 'PROCESSING', 12.30, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(3, 3, 'COMPLETED', 5.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(4, 1, 'PENDING', 15.20, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(5, 2, 'PROCESSING', 22.50, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(6, 3, 'COMPLETED', 10.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(7, 4, 'PENDING', 18.30, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(8, 5, 'CANCELLED', 5.40, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(9, 6, 'PROCESSING', 25.10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(10, 7, 'COMPLETED', 14.70, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(11, 8, 'PENDING', 9.80, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(12, 9, 'PROCESSING', 30.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(13, 10, 'COMPLETED', 12.50, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(14, 1, 'PENDING', 16.90, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(15, 2, 'CANCELLED', 8.20, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(16, 3, 'PROCESSING', 21.40, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(17, 4, 'COMPLETED', 13.60, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(18, 5, 'PENDING', 17.80, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(19, 6, 'PROCESSING', 24.50, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(20, 7, 'CANCELLED', 7.30, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(21, 8, 'COMPLETED', 11.90, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(22, 9, 'PENDING', 19.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(23, 10, 'PROCESSING', 14.20, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(24, 1, 'COMPLETED', 22.10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(25, 2, 'PENDING', 10.40, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(26, 3, 'CANCELLED', 15.70, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(27, 4, 'PROCESSING', 18.90, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(28, 5, 'COMPLETED', 12.30, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(29, 6, 'PENDING', 20.50, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(30, 7, 'PROCESSING', 9.10, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(31, 8, 'CANCELLED', 13.80, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(32, 9, 'COMPLETED', 16.40, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(33, 10, 'PENDING', 11.20, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE);

-- Set the last value for the orders table

ALTER SEQUENCE orders_id_seq RESTART WITH 34;  -- Next ID will be 34

-- Заполнение таблицы order_items (с статическим id)
INSERT INTO order_items (id, order_id, product_id, quantity, unit_price, created_at, updated_at, created_by, updated_by, is_active)
VALUES
(1, 1, 1, 2, 2.50, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(2, 1, 2, 1, 3.50, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(3, 2, 3, 3, 2.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(4, 2, 4, 2, 4.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(5, 3, 5, 1, 3.20, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(6, 3, 6, 4, 2.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(7, 4, 7, 2, 6.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(8, 4, 8, 1, 7.50, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(9, 5, 9, 3, 5.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(10, 5, 10, 2, 4.50, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(11, 6, 11, 1, 5.50, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(12, 6, 12, 4, 5.50, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(13, 7, 13, 2, 4.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(14, 7, 14, 3, 4.80, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(15, 8, 15, 1, 3.20, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(16, 8, 16, 2, 3.50, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(17, 9, 17, 4, 3.50, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(18, 9, 18, 1, 3.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(19, 10, 19, 3, 2.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(20, 10, 20, 2, 3.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(21, 11, 1, 1, 2.50, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(22, 11, 3, 2, 2.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(23, 12, 5, 3, 3.20, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(24, 12, 7, 1, 6.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(25, 13, 9, 2, 5.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(26, 13, 11, 4, 5.50, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(27, 14, 13, 1, 4.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(28, 14, 15, 3, 3.20, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(29, 15, 17, 2, 3.50, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE),
(30, 15, 19, 1, 2.00, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, NULL, NULL, TRUE);

-- Set the last value for the order_items table
ALTER SEQUENCE order_items_id_seq RESTART WITH 31;  -- Next ID will be 31