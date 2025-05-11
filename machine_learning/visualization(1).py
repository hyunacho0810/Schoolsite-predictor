# 시각화2 잔차 그래프
residuals = y_test - y_test_pred
plt.figure(figsize=(10, 6))
plt.scatter(y_test, residuals, color='green')
plt.xlabel('Actual')
plt.ylabel('Residuals')
plt.title('Residuals Plot')
plt.axhline(y=0, color='red', linestyle='--')
plt.show()