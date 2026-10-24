# Inject'ga asoslangan bogʻliqliklarni inyeksiya qilish

Inyeksiya qilinadigan servis yaratish — Angular'dagi bogʻliqliklarni inyeksiya qilish (DI) tizimining birinchi qismi. Servisni komponentga qanday inyeksiya qilasiz? Angular'da tegishli kontekstda ishlatish mumkin boʻlgan `inject()` deb nomlangan qulay funksiya mavjud.

NOTE: Inyeksiya kontekstlari bu darslik doirasidan tashqarida, lekin ular haqida [bogʻliqliklarni inyeksiya qilish (DI) asoslari qoʻllanmasida](/essentials/dependency-injection) va [DI konteksti qoʻllanmasida](guide/di/dependency-injection-context) koʻproq bilib olishingiz mumkin.

Bu mashgʻulotda servisni qanday inyeksiya qilish va uni komponentda ishlatishni oʻrganasiz.

<hr>

Klass xususiyatlarini DI tizimi taqdim etgan qiymatlar bilan ishga tushirish koʻpincha foydali boʻladi. Mana bir misol:

```ts {highlight:[3]}
@Component({...})
class PetCareDashboard {
  petRosterService = inject(PetRosterService);
}
```

<docs-workflow>

<docs-step title="`CarService`'ni inyeksiya qiling {#inject-the-carservice}">

`app.ts` faylida `inject()` funksiyasidan foydalanib `CarService`'ni inyeksiya qiling va uni `carService` deb nomlangan xususiyatga tayinlang

NOTE: `carService` xususiyati va `CarService` klassi oʻrtasidagi farqga eʼtibor bering.

</docs-step>

<docs-step title="`carService` nusxasidan foydalaning {#use-the-carservice-instance}">

`inject(CarService)` chaqiruvi sizga ilovangizda ishlatishingiz mumkin boʻlgan `CarService` nusxasini (instance) berdi, u `carService` xususiyatida saqlanadi.

`display` xususiyatini quyidagi tarzda ishga tushiring:

```ts
display = this.carService.getCars().join(' ⭐️ ');
```

</docs-step>

<docs-step title="`App` shablonini yangilang {#update-the-app-template}">

`app.ts` faylidagi komponent shablonini quyidagi kod bilan yangilang:

```ts
template: `<p>Car Listing: {{ display }}</p>`,
```

</docs-step>

</docs-workflow>

Siz hozirgina birinchi servisingizni komponentga inyeksiya qildingiz — ajoyib harakat.
