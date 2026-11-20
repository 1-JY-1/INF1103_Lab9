FROM python:3.11-slim
WORKDIR /app
COPY testprogram.py inventory.py product.py canbeshipped.py supplier.py order.py orderline.py DiscountStrategy.py .
COPY productfactory.py products.csv .
CMD ["python", "testprogram.py"]