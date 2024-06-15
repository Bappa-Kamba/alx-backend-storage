-- Create trigger to decrease the quantity of an item in the items table after adding a new order.
CREATE TRIGGER after_order_insert
AFTER INSERT ON orders
FOR EACH ROW
BEGIN
    UPDATE items
    SET quantity = quantity - NEW.quantity
    WHERE name = NEW.item_name;
END;