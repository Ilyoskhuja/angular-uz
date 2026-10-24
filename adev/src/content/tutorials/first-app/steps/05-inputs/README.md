# Komponentga input parametri qoʻshing

Bu darslik darsi komponent `input`'ini yaratish va undan komponentni moslashtirish uchun maʼlumot uzatishda foydalanishni koʻrsatadi.

<docs-video src="https://www.youtube.com/embed/eM3zi_n7lNs?si=WvRGFSkW_7_zDIFD&amp;start=241"/>

NOTE: Bu video eskiroq sintaksisni aks ettiradi, lekin asosiy tushunchalar oʻz kuchini saqlab qoladi.

## Nimalarni oʻrganasiz {#what-youll-learn}

Ilovangizning `HousingLocation` shablonida input qabul qiluvchi `HousingLocation` xususiyati paydo boʻladi.

## Input'larning konseptual koʻrinishi {#conceptual-preview-of-inputs}

[Input'lar](api/core/input) komponentlarga ota (parent) komponentdan uzatilishi mumkin boʻlgan maʼlumotlarni belgilash imkonini beradi.

Bu darsda `HousingLocation` komponentida koʻrsatiladigan maʼlumotlarni moslashtirish imkonini beruvchi `input` xususiyatini belgilaysiz.

Koʻproq maʼlumotni [Input xususiyatlari bilan maʼlumot qabul qilish](guide/components/inputs) va [Output'lar bilan maxsus hodisalar](guide/components/outputs) qoʻllanmalarida bilib oling.

<docs-workflow>

<docs-step title="input() funksiyasini import qiling">
Kod muharririda `@angular/core`'dan `input` yordamchi metodini va `../housinglocation`'dan `HousingLocationInfo` interfeysini `HousingLocation` komponentiga import qiling.

<docs-code header="housing-location.ts faylida input va HousingLocationInfo'ni import qiling" path="adev/src/content/tutorials/first-app/steps/06-property-binding/src/app/housing-location/housing-location.ts" visibleLines="[1,2]"/>

</docs-step>

<docs-step title="Input xususiyatini qoʻshing">
`housingLocation` nomli majburiy xususiyat qoʻshing va uni `HousingLocationInfo` turi bilan `input.required()` orqali boshlangʻich qiymat bilan taʼminlang.

  <docs-code header="housing-location.ts faylida input xususiyatini eʼlon qiling" path="adev/src/content/tutorials/first-app/steps/06-property-binding/src/app/housing-location/housing-location.ts" visibleLines="[10]"/>

Ota komponent qiymat berishi shart ekanini bildirish uchun `input` ustida `required` metodini chaqirishingiz kerak. Bizning misol ilovamizda bu qiymat har doim uzatilishini bilamiz — bu ataylab shunday qilingan. `.required()` chaqiruvi TypeScript kompilyatori buni majburiy qilishini va bu komponent shablonda ishlatilganda xususiyatni null boʻlmaydigan (non-nullable) deb hisoblashini taʼminlaydi.

</docs-step>

<docs-step title="Input'ga maʼlumot uzating">
`housingLocation` qiymatini `Home` komponentidan HousingLocation komponentining `housingLocation` xususiyatiga yuboring.

<docs-code language="angular-ts" header="home.ts faylida HousingLocation uchun input xususiyatini eʼlon qiling" path="adev/src/content/tutorials/first-app/steps/06-property-binding/src/app/home/home.ts" visibleLines="[16]"/>

</docs-step>

</docs-workflow>

SUMMARY: Bu darsda yangi `input` xususiyatini yaratdingiz. Shuningdek, signal qiymati har doim aniqlangan boʻlishini taʼminlash uchun `.required` metodidan foydalandingiz.

<docs-pill-row>
  <docs-pill href="guide/components/inputs" title="Input xususiyatlari bilan maʼlumot qabul qilish"/>
  <docs-pill href="guide/components/outputs" title="Output'lar bilan maxsus hodisalar"/>
</docs-pill-row>