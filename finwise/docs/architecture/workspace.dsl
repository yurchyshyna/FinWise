workspace "FinWise" "Персональний фінансовий консультант" {

  model {
    user = person "Користувач" "Веде облік доходів і витрат"
    bank = softwareSystem "Банк" "Надає операції за згодою користувача (банківський API)" "External"
    notify = softwareSystem "Сервіс сповіщень" "Доставляє повідомлення користувачу (email, месенджер)" "External"

    finwise = softwareSystem "FinWise" "Облік, категоризація, ліміти та прогноз витрат" {
      web = container "Веб-застосунок" "Інтерфейс, графіки, налаштування" "React"
      api = container "Backend API" "Витрати, категорії, ліміти, прогноз" "Python (FastAPI)"
      worker = container "Фоновий воркер" "Отримання операцій з банку, категоризація, перевірка лімітів" "Python"
      db  = container "База даних" "Операції, категорії, ліміти, налаштування" "PostgreSQL" "Database"
    }

    user -> web "Керує бюджетом, вносить витрати, завантажує виписку" "HTTPS"
    user -> bank "Надає згоду на доступ до даних"
    web -> api "Надсилає запити" "JSON/HTTPS"
    api -> db "Читає та записує дані" "SQL/TCP"
    worker -> db "Зберігає операції, читає ліміти" "SQL/TCP"
    worker -> bank "Отримує операції" "Банківський API"
    worker -> notify "Надсилає сповіщення про ліміти" "HTTPS"

    live = deploymentEnvironment "Production" {
      deploymentNode "Віртуальна приватна мережа" "Ізольована мережа проєкту" "VPC / підмережа" {
        infrastructureNode "Файрвол" "Відкрито лише порти 22, 80 і 443" "Security Group"

        deploymentNode "Linux VM" "Сервер застосунку" "Ubuntu, 2 vCPU, 4 ГБ RAM" {
          deploymentNode "Docker" "Запуск контейнерів застосунку" "Docker Engine" {
            containerInstance web
            containerInstance api
            containerInstance worker
            containerInstance db
            infrastructureNode "Постійне сховище" "Дані бази зберігаються поза контейнером" "Docker volume"
            infrastructureNode "Моніторинг" "Збір метрик сервера та застосунку" "Prometheus"
          }
        }
      }
    }
  }

  views {
    systemContext finwise "Context" {
      include *
      autolayout tb
    }

    container finwise "Containers" {
      include *
      autolayout tb
    }

    deployment finwise "Production" "Deployment" {
      include *
      autolayout lr
    }

    styles {
      element "Person" {
        shape Person
        background #430847
        color #ffffff
      }
      element "External" {
        background #914197
        color #ffffff
      }
      element "Database" {
        shape Cylinder
        background #9d809f
        color #ffffff
      }
    }

    theme default
  }
}