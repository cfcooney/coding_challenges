# Shopping Cart System
import math

class Product:
    def __init__(self, id, name, price, category):
        self.id = id
        self.name = name
        self.price = price
        self.category = category
    
    def get_discounted_price(self, discount_percent):
        return self.price - (self.price * discount_percent / 100)

class ShoppingCart:
    def __init__(self):
        self.items = {}
        self.discount = 0
    
    def add_item(self, product, quantity):
        if product.id in self.items:
            self.items[product.id]['quantity'] = self.items[product.id]['quantity'] + quantity
        else:
            self.items[product.id] = {'product': product, 'quantity': quantity}
    
    def remove_item(self, product_id, quantity):
        if product_id in self.items:
            if self.items[product_id]['quantity'] > quantity:
                self.items[product_id]['quantity'] = self.items[product_id]['quantity'] - quantity
            else:
                del self.items[product_id]
    
    def calculate_total(self):
        total = 0
        for item_id in self.items:
            item = self.items[item_id]
            if self.discount > 0:
                price = item['product'].get_discounted_price(self.discount)
            else:
                price = item['product'].price
            total = total + (price * item['quantity'])
        return total
    
    def apply_discount(self, discount_percent):
        if discount_percent >= 0 and discount_percent <= 100:
            self.discount = discount_percent
    
    def get_item_count(self):
        count = 0
        for item_id in self.items:
            count = count + self.items[item_id]['quantity']
        return count
    
    def clear_cart(self):
        self.items = {}
        self.discount = 0
    
    def get_items_by_category(self, category):
        result = []
        for item_id in self.items:
            item = self.items[item_id]
            if item['product'].category == category:
                result.append(item)
        return result
    
    def calculate_shipping(self):
        total = self.calculate_total()
        if total > 100:
            return 0
        elif total > 50:
            return 5.99
        else:
            return 9.99
    
    def get_cart_summary(self):
        subtotal = self.calculate_total()
        shipping = self.calculate_shipping()
        total = subtotal + shipping
        return {
            'subtotal': subtotal,
            'shipping': shipping,
            'total': total,
            'item_count': self.get_item_count()
        }

if __name__ == '__main__':
    # Test the shopping cart
    p1 = Product(1, "Laptop", 999.99, "Electronics")
    p2 = Product(2, "Mouse", 29.99, "Electronics")
    p3 = Product(3, "Book", 19.99, "Books")

    cart = ShoppingCart()
    cart.add_item(p1, 1)
    cart.add_item(p2, 2)
    cart.add_item(p3, 1)

    print("Cart summary:", cart.get_cart_summary())

"""
REFACTORING REVIEW - SHOPPING CART SYSTEM
=========================================

CURRENT STATE ANALYSIS:
----------------------

AREAS NEEDING IMPROVEMENT (NOT YET ADDRESSED):
---------------------------------------------

1. **Missing Type Hints** ❌ CRITICAL
   - No type annotations on any methods or parameters
   - Product.__init__ parameters lack types
   - ShoppingCart methods missing return types and parameter types
   - Should add: from typing import Dict, List, Union, Optional

2. **No Documentation** ❌ CRITICAL  
   - Zero docstrings throughout the codebase
   - No method descriptions or parameter explanations
   - Missing class-level documentation

3. **No Input Validation** ❌ CRITICAL
   - Product constructor accepts any values (price could be negative)
   - add_item() doesn't validate quantity (could be negative or zero)
   - remove_item() doesn't validate parameters
   - apply_discount() silently ignores invalid values instead of raising exceptions

4. **Poor Error Handling** ❌ CRITICAL
   - No exceptions raised for invalid operations
   - Silent failures in apply_discount()
   - No validation in remove_item() for non-existent items

5. **Inefficient Code Patterns** ⚠️ IMPORTANT
   - Manual arithmetic: `quantity = quantity + 1` instead of `quantity += 1`
   - Verbose loops instead of list comprehensions
   - Multiple calls to calculate_total() in get_cart_summary()
   - Manual iteration instead of sum() function

6. **Magic Numbers** ⚠️ IMPORTANT
   - Hardcoded shipping thresholds: 100, 50
   - Hardcoded shipping costs: 5.99, 9.99
   - Should be class constants

7. **Missing Edge Case Handling** ⚠️ IMPORTANT
   - What happens if quantity becomes negative in remove_item()?
   - No handling for removing more items than exist
   - No validation for duplicate product IDs

8. **Unused Import** ⚠️ MINOR
   - `import math` is not used anywhere in the code

9. **No __name__ == '__main__' Guard** ⚠️ MINOR
   - Test code runs on import instead of only when executed directly

REFACTORING PRIORITIES:
----------------------

**HIGH PRIORITY:**
1. Add comprehensive type hints
2. Add docstrings to all classes and methods  
3. Implement input validation with proper exceptions
4. Add error handling for edge cases

**MEDIUM PRIORITY:**
5. Extract magic numbers to constants
6. Optimize inefficient loops and calculations
7. Use += operators instead of manual arithmetic

**LOW PRIORITY:**  
8. Remove unused imports
9. Add __name__ == '__main__' guard (✅ DONE)

SUGGESTED IMPROVEMENTS TO IMPLEMENT:
----------------------------------

**Type Safety:**
- Add Union[int, float] for prices and quantities
- Use Dict[int, Dict[str, Union[Product, int]]] for items
- Return types for all methods

**Validation:**
- Validate price > 0 in Product constructor  
- Validate quantity > 0 in add_item()
- Check if product exists before removal
- Raise ValueError for invalid discount percentages

**Performance:**
- Use sum() and list comprehensions
- Cache calculate_total() result in get_cart_summary()
- Use collections.defaultdict for items storage

**Code Quality:**
- Extract shipping logic to separate method with constants
- Create helper methods for item validation
- Add comprehensive docstrings with Args/Returns sections

OVERALL ASSESSMENT:
------------------
🔴 **Status**: Original code - no refactoring completed yet
🎯 **Goal**: Transform from basic script to production-ready code
📝 **Next Steps**: Start with type hints and validation, then move to optimization

This code provides a solid foundation but needs significant refactoring to meet professional standards for maintainability, type safety, and error handling.
"""