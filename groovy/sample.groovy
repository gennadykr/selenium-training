import org.openqa.selenium.*
import org.openqa.selenium.firefox.*

File profileDir = new File("C:/GitHub/selenium-training/groovy/4uxxq5yw.microphone");
FirefoxProfile profile = new FirefoxProfile(profileDir)
driver = new FirefoxDriver(profile)
driver.get("http://ya.ru/")
input = driver.findElement(By.name("text"))
input.sendKeys("документация selenium")
button = driver.findElement(By.cssSelector("*.suggest2-form__button"))
button.click()
driver.quit()

// Reference:
// http://selenium2.ru/articles/47-groovy-console.html
//