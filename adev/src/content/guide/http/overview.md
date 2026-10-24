# HTTP orqali backend servislari bilan aloqani tushunish

Koʻpchilik front-end ilovalar maʼlumotlarni yuklab olish yoki yuklash va boshqa back-end servislariga murojaat qilish uchun server bilan HTTP protokoli orqali aloqa qilishi kerak. Angular Angular ilovalari uchun HTTP klient API'sini — `@angular/common/http` ichidagi `HttpClient` servis klassini taqdim etadi.

## HTTP klient servisining imkoniyatlari {#http-client-service-features}

HTTP klient servisi quyidagi asosiy imkoniyatlarni taklif qiladi:

- [Tiplangan javob qiymatlarini](guide/http/making-requests#fetching-json-data) soʻrash imkoniyati
- Soddalashtirilgan [xatolarni qayta ishlash](guide/http/making-requests#handling-request-failure)
- Soʻrov va javobni [ushlab qolish (interception)](guide/http/interceptors)
- Mustahkam [test vositalari](guide/http/testing)

## Keyingi qadamlar {#whats-next}

<docs-pill-row>
  <docs-pill href="guide/http/setup" title="HttpClient'ni sozlash"/>
  <docs-pill href="guide/http/making-requests" title="HTTP soʻrovlarini yuborish"/>
</docs-pill-row>
