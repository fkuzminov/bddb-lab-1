// Найти клиентов, совершивших заказы на сумму выше определённого
// значения.

db.customers.aggregate([
    {
        $lookup: {
            from: "orders",
            localField: "_id",
            foreignField: "customer_id",
            as: "orders"
        }
    },
    {
        $project: {
            _id: 0,
            email: 1,
            total_amount: { $sum: "$orders.total_amount" }
        }
    },
    { $match: { total_amount: { $gte: 10000 } } }, // 10000 etc
]);