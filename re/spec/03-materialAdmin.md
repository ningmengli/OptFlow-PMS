# 03｜模块 materialAdmin 物资/商品/SKU

> 由 `re/gen-spec.py` 自动生成，数据源 `re/pages.json` + `re/page-api-map.json`（视光之家 6.9，2026-09-30 观测）。
> **本册只记录生产实测到的结构，不含任何推测。**模板中未出现的字段一律不写。

| 项 | 值 |
|---|---|
| 模块目录 | `views/materialAdmin/` |
| 中文名 | 物资/商品/SKU |
| 开发波次 | W5 |
| 页面数 | **84** |
| 端点数（去重） | **118** |

## §1 页面清单

| # | state | url | 模板 | 控制器 | 端点 |
|--:|---|---|---|---|--:|
| 1 | `addDelivery` | `/addDelivery` | `views/materialAdmin/addDelivery.html` | `addDeliveryCtrl` | 6 |
| 2 | `goods.addCompanyDelivery` | `/addCompanyDelivery?storehouseId&productType` | `views/materialAdmin/addDelivery.html` | `addDeliveryCtrl` | 6 |
| 3 | `addDeliveryCustomer` | `/addDeliveryCustomer` | `views/materialAdmin/addDeliveryCustomer.html` | `addDeliveryCustomerCtrl` | 5 |
| 4 | `addInventory` | `/addInventory` | `views/materialAdmin/addInventory.html` | `addInventoryCtrl` | 6 |
| 5 | `goods.addCompanyInventory` | `/addCompanyInventory?storehouseId` | `views/materialAdmin/addInventory.html` | `addInventoryCtrl` | 6 |
| 6 | `addMultiDelivery` | `/addMultiDelivery?storehouseId` | `views/materialAdmin/addMultiDelivery.html` | `addMultiDeliveryCtrl` | 6 |
| 7 | `goods.addCompanyMultiDelivery` | `/addCompanyMultiDelivery?storehouseId` | `views/materialAdmin/addMultiDelivery.html` | `addMultiDeliveryCtrl` | 6 |
| 8 | `addMultiReceipts` | `/addMultiReceipts` | `views/materialAdmin/addMultiReceipts.html` | `addMultiReceiptsCtrl` | 6 |
| 9 | `goods.addCompanyMultiReceipts` | `/addCompanyMultiReceipts?storehouseId` | `views/materialAdmin/addMultiReceipts.html` | `addMultiReceiptsCtrl` | 6 |
| 10 | `goods.addProductBivariateTable` | `/addProductBivariateTable?storehouseId&productId` | `views/materialAdmin/addProductBivariateTable.html` | `addProductBivariateTableCtrl` | 4 |
| 11 | `goods.addProductDelivery` | `/addProductDelivery?storehouseId&productType` | `views/materialAdmin/addProductDelivery.html` | `addProductDeliveryCtrl` | 6 |
| 12 | `goods.addProductInventory` | `/addProductInventory?storehouseId` | `views/materialAdmin/addProductInventory.html` | `addProductInventoryCtrl` | 5 |
| 13 | `addPurchaseRequest` | `/addPurchaseRequest` | `views/materialAdmin/addPurchaseRequest.html` | `addPurchaseRequestCtrl` | 0 |
| 14 | `purchase.addPurchasement` | `/addPurchasement` | `views/materialAdmin/addPurchasement.html` | `addPurchasementCtrl` | 8 |
| 15 | `goods.addCompanyReceipt` | `/addCompanyReceipt?storehouseId` | `views/materialAdmin/addReceipt.html` | `addReceiptCtrl` | 7 |
| 16 | `addReceipt` | `/addReceipt` | `views/materialAdmin/addReceipt.html` | `addReceiptCtrl` | 7 |
| 17 | `purchase.addSalePurchase` | `/addSalePurchase` | `views/materialAdmin/addSalePurchase.html` | `addSalePurchaseCtrl` | 6 |
| 18 | `addStockChange` | `/addStockChange` | `views/materialAdmin/addStockChange.html` | `addStockChangeCtrl` | 4 |
| 19 | `goods.addStockCompanyChange` | `/addStockCompanyChange?storehouseId&status` | `views/materialAdmin/addStockCompanyChange.html` | `addStockChangeCtrl` | 4 |
| 20 | `goods.addStockProductChange` | `/addStockProductChange?storehouseId&status` | `views/materialAdmin/addStockProductChange.html` | `addStockProductChangeCtrl` | 6 |
| 21 | `adminBill` | `/adminBill` | `views/materialAdmin/adminBill.html` | `adminBillCtrl` | 0 |
| 22 | `adminBillDetial` | `/adminBillDetial?supplierId` | `views/materialAdmin/adminBillDetial.html` | `adminBillDetialCtrl` | 10 |
| 23 | `adminBillOneDetial` | `/adminBillOneDetial?supplierId&stockSettlementId` | `views/materialAdmin/adminBillOneDetial.html` | `adminBillOneDetialCtrl` | 0 |
| 24 | `deliveryDelete` | `/deliveryDelete?stockOutId` | `views/materialAdmin/deliveryDelete.html` | `deliveryDeleteCtrl` | 0 |
| 25 | `goods.deliveryCompanyDetail` | `/deliveryCompanyDetail?stockOutId` | `views/materialAdmin/deliveryDetail.html` | `deliveryDetailCtrl` | 1 |
| 26 | `deliveryDetail` | `/deliveryDetail?stockOutId` | `views/materialAdmin/deliveryDetail.html` | `deliveryDetailCtrl` | 1 |
| 27 | `deliveryDetailCustomer` | `/deliveryDetailCustomer?stockOutId` | `views/materialAdmin/deliveryDetailCustomer.html` | `deliveryDetailCtrl` | 1 |
| 28 | `goods.deliveryCompanyModify` | `/deliveryCompanyModify?stockOutId` | `views/materialAdmin/deliveryModify.html` | `deliveryModifyCtrl` | 4 |
| 29 | `deliveryModify` | `/deliveryModify?stockOutId` | `views/materialAdmin/deliveryModify.html` | `deliveryModifyCtrl` | 4 |
| 30 | `deliveryModifyCustomer` | `/deliveryModifyCustomer?stockOutId` | `views/materialAdmin/deliveryModifyCustomer.html` | `deliveryModifyCustomerCtrl` | 0 |
| 31 | `goods.deliveryProductDetail` | `/deliveryProductDetail?stockOutId` | `views/materialAdmin/deliveryProductDetail.html` | `deliveryProductModifyCtrl` | 5 |
| 32 | `goods.deliveryProductModify` | `/deliveryProductModify?stockOutId` | `views/materialAdmin/deliveryProductModify.html` | `deliveryProductModifyCtrl` | 5 |
| 33 | `goods` | `/goods` | `views/materialAdmin/goods.html` | `goodsCtrl` | 7 |
| 34 | `inventoryDetail` | `/inventoryDetail?stockTakingId` | `views/materialAdmin/inventoryDetail.html` | `inventoryDetailCtrl` | 0 |
| 35 | `goods.inventoryCompanyDetail` | `/inventoryCompanyDetail?stockTakingId` | `views/materialAdmin/inventoryDetail.html` | `inventoryDetailCtrl` | 0 |
| 36 | `inventoryModify` | `/inventoryModify?stockTakingId` | `views/materialAdmin/inventoryModify.html` | `inventoryModifyCtrl` | 0 |
| 37 | `goods.inventoryCompanyModify` | `/inventoryCompanyModify?stockTakingId` | `views/materialAdmin/inventoryModify.html` | `inventoryModifyCtrl` | 0 |
| 38 | `goods.inventoryProductDetail` | `/inventoryProductDetail?stockTakingId` | `views/materialAdmin/inventoryProductDetail.html` | `inventoryProductModifyCtrl` | 0 |
| 39 | `goods.inventoryProductModify` | `/inventoryProductModify?stockTakingId` | `views/materialAdmin/inventoryProductModify.html` | `inventoryProductModifyCtrl` | 0 |
| 40 | `materialDelivery` | `/materialDelivery` | `views/materialAdmin/materialDelivery.html` | `materialDeliveryCtrl` | 14 |
| 41 | `goods.materialCompanyDelivery` | `/materialCompanyDelivery` | `views/materialAdmin/materialDelivery.html` | `materialDeliveryCtrl` | 14 |
| 42 | `materialImportRecord` | `/materialImportRecord` | `views/materialAdmin/materialImportRecord.html` | `materialImportRecordCtrl` | 0 |
| 43 | `goods.companyImportRecord` | `/companyImportRecord?storehouseId` | `views/materialAdmin/materialImportRecord.html` | `materialImportRecordCtrl` | 0 |
| 44 | `materialInventory` | `/materialInventory` | `views/materialAdmin/materialInventory.html` | `materialInventoryCtrl` | 0 |
| 45 | `goods.materialCompanyInventory` | `/materialCompanyInventory` | `views/materialAdmin/materialInventory.html` | `materialInventoryCtrl` | 0 |
| 46 | `materialOutportRecord` | `/materialOutportRecord?storehouseId` | `views/materialAdmin/materialOutportRecord.html` | `materialOutportRecordCtrl` | 0 |
| 47 | `goods.materialCompanyOutportRecord` | `/materialCompanyOutportRecord?storehouseId` | `views/materialAdmin/materialOutportRecord.html` | `materialOutportRecordCtrl` | 0 |
| 48 | `purchase.materialPurchase` | `/materialPurchase` | `views/materialAdmin/materialPurchase.html` | `materialPurchaseCtrl` | 14 |
| 49 | `purchase.materialPurchaseBackGoods` | `/materialPurchaseBackGoods?stockPurchaseOutId&storehouseId` | `views/materialAdmin/materialPurchaseBackGoods.html` | `materialPurchaseBackGoodsCtrl` | 0 |
| 50 | `purchase.materialPurchaseBackLook` | `/materialPurchaseBackLook?stockPurchaseOutId&storehouseId` | `views/materialAdmin/materialPurchaseBackLook.html` | `materialPurchaseBackLookCtrl` | 5 |
| 51 | `purchase.materialPurchaseBackOne` | `/materialPurchaseBackOne?id&type&stockPurchaseOutId` | `views/materialAdmin/materialPurchaseBackOne.html` | `materialPurchaseBackOneCtrl` | 0 |
| 52 | `materialPurchaseRequest` | `/materialPurchaseRequest` | `views/materialAdmin/materialPurchaseRequest.html` | `materialPurchaseRequestCtrl` | 11 |
| 53 | `purchase.materialPurchaseReturn` | `/materialPurchaseReturn` | `views/materialAdmin/materialPurchaseReturn.html` | `materialPurchaseReturnCtrl` | 0 |
| 54 | `goods.companyMaterialReceipts` | `/companyMaterialReceipts` | `views/materialAdmin/materialReceipts.html` | `materialReceiptsCtrl` | 4 |
| 55 | `materialReceipts` | `/materialReceipts` | `views/materialAdmin/materialReceipts.html` | `materialReceiptsCtrl` | 4 |
| 56 | `goods.modifyStockCompanyChange` | `/modifyStockCompanyChange?id&storehouseId` | `views/materialAdmin/modifyStockChange.html` | `modifyStockChangeCtrl` | 4 |
| 57 | `modifyStockChange` | `/modifyStockChange?id` | `views/materialAdmin/modifyStockChange.html` | `modifyStockChangeCtrl` | 4 |
| 58 | `goods.modifyStockProductChange` | `/modifyStockProductChange?id&storehouseId` | `views/materialAdmin/modifyStockProductChange.html` | `modifyStockProductChangeCtrl` | 6 |
| 59 | `purchaseDetail` | `/purchaseDetail?purchaseId` | `views/materialAdmin/purchaseDetail.html` | `purchaseDetailCtrl` | 0 |
| 60 | `purchase.purchaseModify` | `/purchaseModify?purchaseId` | `views/materialAdmin/purchaseModify.html` | `purchaseModifyCtrl` | 25 |
| 61 | `purchase.purchaseReciept` | `/purchaseReciept?purchaseId` | `views/materialAdmin/purchaseReciept.html` | `purchaseRecieptCtrl` | 0 |
| 62 | `purchase.purchaseRecieptDetail` | `/purchaseRecieptDetail?purchaseId` | `views/materialAdmin/purchaseRecieptDetail.html` | `purchaseRecieptCtrl` | 0 |
| 63 | `purchase.purchaseRequestCheck` | `/purchaseRequestCheck` | `views/materialAdmin/purchaseRequestCheck.html` | `purchaseRequestCheckCtrl` | 0 |
| 64 | `purchaseRequestCheckDetail` | `/purchaseRequestCheckDetail?purchaseRequestId` | `views/materialAdmin/purchaseRequestCheckDetail.html` | `purchaseRequestCheckDetailCtrl` | 0 |
| 65 | `purchaseRequestDetail` | `/purchaseRequestDetail?purchaseRequestId` | `views/materialAdmin/purchaseRequestDetail.html` | `purchaseRequestModifyCtrl` | 0 |
| 66 | `purchaseRequestModify` | `/purchaseRequestModify?purchaseRequestId` | `views/materialAdmin/purchaseRequestModify.html` | `purchaseRequestModifyCtrl` | 0 |
| 67 | `goods.receiptCompanyDetail` | `/receiptCompanyDetail?stockInId` | `views/materialAdmin/receiptDetail.html` | `receiptDetailCtrl` | 6 |
| 68 | `receiptDetail` | `/receiptDetail?stockInId` | `views/materialAdmin/receiptDetail.html` | `receiptDetailCtrl` | 6 |
| 69 | `receiptDetailCustomer` | `/receiptDetailCustomer?stockInId` | `views/materialAdmin/receiptDetailCustomer.html` | `receiptDetailCtrl` | 6 |
| 70 | `receiptInvalid` | `/receiptInvalid?stockInId` | `views/materialAdmin/receiptInvalid.html` | `receiptInvalidCtrl` | 4 |
| 71 | `goods.receiptCompanyInvalid` | `/receiptCompanyInvalid?stockInId` | `views/materialAdmin/receiptInvalid.html` | `receiptInvalidCtrl` | 4 |
| 72 | `receiptModify` | `/receiptModify?stockInId` | `views/materialAdmin/receiptModify.html` | `receiptModifyCtrl` | 5 |
| 73 | `goods.receiptCompanyModify` | `/receiptCompanyModify?stockInId` | `views/materialAdmin/receiptModify.html` | `receiptModifyCtrl` | 5 |
| 74 | `stockChange` | `/stockChange` | `views/materialAdmin/stockChange.html` | `stockChangeCtrl` | 8 |
| 75 | `goods.stockCompanyChange` | `/stockCompanyChange` | `views/materialAdmin/stockChange.html` | `stockChangeCtrl` | 8 |
| 76 | `stockChangeCheck` | `/stockChangeCheck?id` | `views/materialAdmin/stockChangeCheck.html` | `stockChangeCheckCtrl` | 0 |
| 77 | `goods.stockCompanyChangeCheck` | `/stockCompanyChangeCheck?id&storehouseId` | `views/materialAdmin/stockChangeCheck.html` | `stockChangeCheckCtrl` | 0 |
| 78 | `stockChangeDetail` | `/stockChangeDetail?id` | `views/materialAdmin/stockChangeDetail.html` | `stockChangeDetailCtrl` | 0 |
| 79 | `goods.stockCompanyChangeDetail` | `/stockCompanyChangeDetail?id` | `views/materialAdmin/stockChangeDetail.html` | `stockChangeDetailCtrl` | 0 |
| 80 | `goods.stockProductChangeCheck` | `/stockProductChangeCheck?id&storehouseId` | `views/materialAdmin/stockProductChangeCheck.html` | `stockProductChangeCheckCtrl` | 0 |
| 81 | `goods.stockProductChangeDetail` | `/stockProductChangeDetail?id&storehouseId` | `views/materialAdmin/stockProductChangeDetail.html` | `modifyStockProductChangeCtrl` | 6 |
| 82 | `viewStockList` | `/viewStockList` | `views/materialAdmin/viewStockList.html` | `stockListCtrl` | 6 |
| 83 | `viewStockList2` | `/viewStockList2` | `views/materialAdmin/viewStockList2.html` | `stockListsCtrl` | 10 |
| 84 | `viewStockList3` | `/viewStockList3` | `views/materialAdmin/viewStockList3.html` | `stockListssCtrl` | 6 |

## §2 端点清单（去重 118 个）

- `POST /admin/cancelStockIn.json`
- `POST /admin/cancelStockInSku.json`
- `POST /admin/cancelStockOutForPurchaseOut.json`
- `POST /admin/cancelStockPurchase.json`
- `POST /admin/changeToProductSkuVoList.json`
- `POST /admin/checkDeletePurchaseRequestSku.json`
- `POST /admin/checkDeleteStockPurchaseSku.json`
- `POST /admin/checkStockIn.json`
- `POST /admin/checkStockOut.json`
- `POST /admin/checkStockTaking.json`
- `POST /admin/checkStockTransfer.json`
- `POST /admin/commitPurchaseRequest.json`
- `POST /admin/commitPurchaseRequestList.json`
- `POST /admin/commitStockOutByProductSku.json`
- `POST /admin/commitStockPurchase.json`
- `POST /admin/commitStockPurchaseIn.json`
- `POST /admin/commitStockPurchaseList.json`
- `POST /admin/commitStockPurchaseOut.json`
- `POST /admin/commitStockTakingByProductSku.json`
- `POST /admin/commitStockTransferByProductSku.json`
- `POST /admin/completeStockTransfer.json`
- `POST /admin/completeSupplierSettlement.json`
- `POST /admin/completeSupplierSettlementBack.json`
- `POST /admin/computePrice.json`
- `POST /admin/createPromotion.json`
- `POST /admin/createPurchaseRequestAndSkuList.json`
- `POST /admin/createStockInAndSkuList.json`
- `POST /admin/createStockInBatchFileTask.json`
- `POST /admin/createStockOutAndSkuList.json`
- `POST /admin/createStockOutBatchFileTask.json`
- `POST /admin/createStockOutByProductSku.json`
- `POST /admin/createStockPurchaseAndSkuList.json`
- `POST /admin/createStockPurchaseFromRequest.json`
- `POST /admin/createStockPurchaseInAndSkuList.json`
- `POST /admin/createStockPurchaseOutAndSkuList.json`
- `POST /admin/createStockSettlementFromTranferOrBack.json`
- `POST /admin/createStockTakingAndSkuList.json`
- `POST /admin/createStockTakingByProductSku.json`
- `POST /admin/createStockTransferAndSkuList.json`
- `POST /admin/createStockTransferByProductSku.json`
- `POST /admin/delStockPurchaseOutByIdBeforeCheckd.json`
- `POST /admin/deletePurchaseRequest.json`
- `POST /admin/deleteStockIn.json`
- `POST /admin/deleteStockOut.json`
- `POST /admin/deleteStockPurchase.json`
- `POST /admin/deleteStockTaking.json`
- `POST /admin/deleteStockTransfer.json`
- `POST /admin/getBrandListOfProduct.json`
- `POST /admin/getCategoryTree2Level.json`
- `POST /admin/getChildrenLinkAndCode.json`
- `POST /admin/getCompanyList.json`
- `POST /admin/getCorpInfo.json`
- `POST /admin/getLimitStorehouseListOfCorp.json`
- `POST /admin/getProductSkuCountInStorehouseVoList.json`
- `POST /admin/getProductSkuExistCountVoList.json`
- `POST /admin/getProductSkuInVoList.json`
- `POST /admin/getProductSkuPlaneVo.json`
- `POST /admin/getProductSkuVoList.json`
- `POST /admin/getProductVoList.json`
- `POST /admin/getPurchaseRequestVo.json`
- `POST /admin/getPurchaseRequestVoList.json`
- `POST /admin/getPurchaseRequestVoListOfCompany.json`
- `POST /admin/getSkuCodeVoListOfStockIn.json`
- `POST /admin/getStockConf.json`
- `POST /admin/getStockCountForTwoDimensionalTable.json`
- `POST /admin/getStockInSkuVo.json`
- `POST /admin/getStockInSkuVoList.json`
- `POST /admin/getStockInSkuVoListOfStockIn.json`
- `POST /admin/getStockInVo.json`
- `POST /admin/getStockInVoList.json`
- `POST /admin/getStockOutProductVoList.json`
- `POST /admin/getStockOutVo.json`
- `POST /admin/getStockOutVoList.json`
- `POST /admin/getStockPurchaseOutList.json`
- `POST /admin/getStockPurchaseOutSkuList.json`
- `POST /admin/getStockPurchaseVo.json`
- `POST /admin/getStockPurchaseVoList.json`
- `POST /admin/getStockPurchaseVoWithExistSkuCount.json`
- `POST /admin/getStockSettlementVoDetail.json`
- `POST /admin/getStockTakingProductVoList.json`
- `POST /admin/getStockTakingVo.json`
- `POST /admin/getStockTakingVoList.json`
- `POST /admin/getStockTransferProductVoList.json`
- `POST /admin/getStockTransferVo.json`
- `POST /admin/getStockTransferVoList.json`
- `POST /admin/getStorehouseListOfMine.json`
- `POST /admin/getStorehouseVo.json`
- `POST /admin/getSupplier.json`
- `POST /admin/getSupplierList.json`
- `POST /admin/getUnPaymentOfStockSettlement.json`
- `POST /admin/isAdminRoleStateOK.json`
- `POST /admin/isPurchaseRequestProcessed.json`
- `POST /admin/mergePurchaseRequestSku.json`
- `POST /admin/reCreateStockPurchaseAndSkuList.json`
- `POST /admin/reSendPurchaseRequest.json`
- `POST /admin/selectCloudPrinterList.json`
- `POST /admin/selectEmployeeByName.json`
- `POST /admin/selectMedicalProductSkuUseVoList.json`
- `POST /admin/selectModelValueList.json`
- `POST /admin/selectSettlementBySupplier.json`
- `POST /admin/selectStockPurchaseInVoList.json`
- `POST /admin/selectStockSettlementVoList.json`
- `POST /admin/selectStorehouseExistSkuCountVoList.json`
- `POST /admin/selectStorehouseVoList.json`
- `POST /admin/sendSkuToCloudPrinter.json`
- `POST /admin/udpateStockOutAndSkuList.json`
- `POST /admin/updatePurchaseRequestAndSkuList.json`
- `POST /admin/updateStockInAndSkuList.json`
- `POST /admin/updateStockOutByProductSku.json`
- `POST /admin/updateStockPurchaseAndSkuList.json`
- `POST /admin/updateStockPurchaseOutSkuList.json`
- `POST /admin/updateStockTakingAndSkuList.json`
- `POST /admin/updateStockTakingByProductSku.json`
- `POST /admin/updateStockTransferAndSkuList.json`
- `POST /admin/updateStockTransferByProductSku.json`
- `POST /admin/verifySettlement.json`
- `POST /admin/viewPurchaseRequestSkuVoList.json`
- `POST /admin/viewStockPurchaseSkuVoList.json`

## §3 逐页字段规格

### 3.1 `addDelivery`

- **URL**：`/addDelivery`
- **模板**：`views/materialAdmin/addDelivery.html`
- **控制器**：`addDeliveryCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createStockOutAndSkuList` | `POST /admin/createStockOutAndSkuList.json` |
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getProductSkuInVoList` | `POST /admin/getProductSkuInVoList.json` |
| `getStorehouseVo` | `POST /admin/getStorehouseVo.json` |
| `selectEmployeeByName` | `POST /admin/selectEmployeeByName.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 出库数量 |
| 7 | 成本价(￥) |
| 8 | 生产日期 |
| 9 | 批号 |
| 10 | 有效期 |
| 11 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `create.outDate` |
| `create.outType` |
| `supplierKeyword` |
| `item.outCount` |
| `obj.storehouseId` |
| `obj.remark` |
| `create.remark` |
| `obj.keyword` |
| `obj.modelKeyword` |
| `product.productSku` |
| `obj.brandId` |
| `select.stockInSkuId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `create.outDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `supplierWord` |
| `item.employeeName` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `item.model1Name` |
| `item.model1` |
| `item.model2Name` |
| `item.model2` |
| `item.unLockExistSkuCount` |
| `item.productionDateLong` |
| `item.batchNo` |
| `item.expiresDateLong` |
| `totalprice` |
| `outCount` |
| `storeName` |
| `item.product.productName` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `province.id` |
| `province.brandName` |
| `getProductListFactory.items` |
| `select.idx` |
| `unLockExistSkuCount` |
| `iten.unLockExistSkuCount` |
| `iten.stockIn.inDate` |
| `iten.storehouse.name` |
| `iten.stockInSku.productionDate` |
| `iten.stockInSku.expiresDate` |
| `iten.stockInSku.batchNo` |
| `ite.modelName` |
| `ite.modelValue` |
| `product.model1Name` |
| `product.model2Name` |
| `iten.stockInSku.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `open1()` |
| `showsupplierList($event)` |
| `searchSupplierList(supplierKeyword,$event)` |
| `selectSupplier(item.id,item.employeeName)` |
| `clearSupplier()` |
| `deleteReceipt($index)` |
| `showAddModal()` |
| `addDelivery()` |
| `selectProductName(item.productSku.id,$index)` |
| `getProductListFactory.nextPage()` |
| `setstockInSkuId(iten.stockInSku.id,$index)` |
| `selectProduct()` |
| `hideProductModal()` |

**跳转到**：`goods.materialCompanyDelivery`, `materialDelivery`

**下拉数据源（ng-options）**

```
x.id as x.name for x in outType
x.id as x.name for x in storehouseArr
```

### 3.2 `goods.addCompanyDelivery`

- **URL**：`/addCompanyDelivery?storehouseId&productType`
- **模板**：`views/materialAdmin/addDelivery.html`
- **控制器**：`addDeliveryCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createStockOutAndSkuList` | `POST /admin/createStockOutAndSkuList.json` |
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getProductSkuInVoList` | `POST /admin/getProductSkuInVoList.json` |
| `getStorehouseVo` | `POST /admin/getStorehouseVo.json` |
| `selectEmployeeByName` | `POST /admin/selectEmployeeByName.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 出库数量 |
| 7 | 成本价(￥) |
| 8 | 生产日期 |
| 9 | 批号 |
| 10 | 有效期 |
| 11 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `create.outDate` |
| `create.outType` |
| `supplierKeyword` |
| `item.outCount` |
| `obj.storehouseId` |
| `obj.remark` |
| `create.remark` |
| `obj.keyword` |
| `obj.modelKeyword` |
| `product.productSku` |
| `obj.brandId` |
| `select.stockInSkuId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `create.outDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `supplierWord` |
| `item.employeeName` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `item.model1Name` |
| `item.model1` |
| `item.model2Name` |
| `item.model2` |
| `item.unLockExistSkuCount` |
| `item.productionDateLong` |
| `item.batchNo` |
| `item.expiresDateLong` |
| `totalprice` |
| `outCount` |
| `storeName` |
| `item.product.productName` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `province.id` |
| `province.brandName` |
| `getProductListFactory.items` |
| `select.idx` |
| `unLockExistSkuCount` |
| `iten.unLockExistSkuCount` |
| `iten.stockIn.inDate` |
| `iten.storehouse.name` |
| `iten.stockInSku.productionDate` |
| `iten.stockInSku.expiresDate` |
| `iten.stockInSku.batchNo` |
| `ite.modelName` |
| `ite.modelValue` |
| `product.model1Name` |
| `product.model2Name` |
| `iten.stockInSku.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `open1()` |
| `showsupplierList($event)` |
| `searchSupplierList(supplierKeyword,$event)` |
| `selectSupplier(item.id,item.employeeName)` |
| `clearSupplier()` |
| `deleteReceipt($index)` |
| `showAddModal()` |
| `addDelivery()` |
| `selectProductName(item.productSku.id,$index)` |
| `getProductListFactory.nextPage()` |
| `setstockInSkuId(iten.stockInSku.id,$index)` |
| `selectProduct()` |
| `hideProductModal()` |

**跳转到**：`goods.materialCompanyDelivery`, `materialDelivery`

**下拉数据源（ng-options）**

```
x.id as x.name for x in outType
x.id as x.name for x in storehouseArr
```

### 3.3 `addDeliveryCustomer`

- **URL**：`/addDeliveryCustomer`
- **模板**：`views/materialAdmin/addDeliveryCustomer.html`
- **控制器**：`addDeliveryCustomerCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createStockOutAndSkuList` | `POST /admin/createStockOutAndSkuList.json` |
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getProductSkuInVoList` | `POST /admin/getProductSkuInVoList.json` |
| `selectEmployeeByName` | `POST /admin/selectEmployeeByName.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品规格信息 |
| 4 | 参数 |
| 5 | 出库数量 |
| 6 | 成本价(￥) |
| 7 | 批次 |
| 8 | 有效期 |
| 9 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `create.outDate` |
| `create.outType` |
| `supplierKeyword` |
| `item.outCount` |
| `obj.storehouseId` |
| `create.remark` |
| `obj.keyword` |
| `product.productSku` |
| `obj.brandId` |
| `select.stockInSkuId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `supplierWord` |
| `item.employeeName` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `item.model1` |
| `item.model2` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.remark` |
| `item.skuCount` |
| `item.skuOutCount` |
| `item.inDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.name` |
| `item.expiresDateLong` |
| `item.batchNo` |
| `item.product.productName` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `province.id` |
| `province.brandName` |
| `getProductListFactory.items` |
| `select.idx` |
| `stockInSkuExistCount` |
| `iten.stockInSkuExistCount` |
| `iten.stockIn.inDate` |
| `iten.storehouse.name` |
| `iten.stockInSku.expiresDate` |
| `iten.stockInSku.batchNo` |
| `ite.modelName` |
| `ite.modelValue` |
| `product.model1Name` |
| `product.model2Name` |
| `iten.stockInSku.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `open1()` |
| `showsupplierList($event)` |
| `searchSupplierList(supplierKeyword,$event)` |
| `selectSupplier(item.id,item.employeeName)` |
| `clearSupplier()` |
| `deleteReceipt($index)` |
| `showAddModal()` |
| `addDelivery()` |
| `selectProductName(item.productSku.id,$index)` |
| `getProductListFactory.nextPage()` |
| `setstockInSkuId(iten.stockInSku.id,$index)` |
| `selectProduct()` |
| `hideProductModal()` |

**跳转到**：`materialDeliveryCustomer`

**下拉数据源（ng-options）**

```
x.id as x.name for x in outType
x.id as x.name for x in storehouseArr
```

### 3.4 `addInventory`

- **URL**：`/addInventory`
- **模板**：`views/materialAdmin/addInventory.html`
- **控制器**：`addInventoryCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createStockTakingAndSkuList` | `POST /admin/createStockTakingAndSkuList.json` |
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getCategoryTree2Level` | `POST /admin/getCategoryTree2Level.json` |
| `getStockInSkuVoList` | `POST /admin/getStockInSkuVoList.json` |
| `getStorehouseVo` | `POST /admin/getStorehouseVo.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表单标签**

| 标签 |
|---|
| 库存小于0 |
| 库存等于0 |
| 库存大于0 |
| 正常 |
| 停用 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 品牌/类目 |
| 2 | 商品信息 |
| 3 | 规格 |
| 4 | 生产日期 |
| 5 | 批次 |
| 6 | 账面数量 |
| 7 | 实际数量 |
| 8 | 盘盈盘亏 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.storehouseId` |
| `obj.brandId` |
| `obj.keyword` |
| `obj.modelKeyword` |
| `obj.lessThanZero` |
| `obj.equalToZero` |
| `obj.moreThanZero` |
| `item.newCount` |
| `pageSize` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `storeName` |
| `province.id` |
| `province.brandName` |
| `item.root.categoryName` |
| `iten.root.categoryName` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockInSku.remark` |
| `item.stockInSku.productionDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.stockIn.gmtCreate` |
| `item.storehouse.name` |
| `item.supplier.supplierName` |
| `item.stockInSku.batchNo` |
| `item.stockInSkuExistCount` |
| `item.stockInSku.skuCount` |
| `item.stockInSku.skuOutCount` |
| `item.newCount` |
| `getStockListFactory.count` |
| `downloadIndex` |
| `pageSize` |
| `getStockListFactory.items.length` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `setCustomer(null)` |
| `setCustomer(1)` |
| `setCustomer(2)` |
| `searchStock()` |
| `setStatus(0)` |
| `setStatus(1)` |
| `downloadModal=true` |
| `chooseCategory(` |
| `chooseCategory(item.root.id,false)` |
| `chooseCategoryId(iten.root.id,$event)` |
| `schoolListFactory.nextPage()` |
| `saveInventory()` |
| `downloadModal=false` |
| `daochu()` |

**跳转到**：`goods.materialCompanyInventory`, `materialInventory`

**下拉数据源（ng-options）**

```
x.id as x.name for x in storehouseArr
```

### 3.5 `goods.addCompanyInventory`

- **URL**：`/addCompanyInventory?storehouseId`
- **模板**：`views/materialAdmin/addInventory.html`
- **控制器**：`addInventoryCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createStockTakingAndSkuList` | `POST /admin/createStockTakingAndSkuList.json` |
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getCategoryTree2Level` | `POST /admin/getCategoryTree2Level.json` |
| `getStockInSkuVoList` | `POST /admin/getStockInSkuVoList.json` |
| `getStorehouseVo` | `POST /admin/getStorehouseVo.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表单标签**

| 标签 |
|---|
| 库存小于0 |
| 库存等于0 |
| 库存大于0 |
| 正常 |
| 停用 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 品牌/类目 |
| 2 | 商品信息 |
| 3 | 规格 |
| 4 | 生产日期 |
| 5 | 批次 |
| 6 | 账面数量 |
| 7 | 实际数量 |
| 8 | 盘盈盘亏 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.storehouseId` |
| `obj.brandId` |
| `obj.keyword` |
| `obj.modelKeyword` |
| `obj.lessThanZero` |
| `obj.equalToZero` |
| `obj.moreThanZero` |
| `item.newCount` |
| `pageSize` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `storeName` |
| `province.id` |
| `province.brandName` |
| `item.root.categoryName` |
| `iten.root.categoryName` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockInSku.remark` |
| `item.stockInSku.productionDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.stockIn.gmtCreate` |
| `item.storehouse.name` |
| `item.supplier.supplierName` |
| `item.stockInSku.batchNo` |
| `item.stockInSkuExistCount` |
| `item.stockInSku.skuCount` |
| `item.stockInSku.skuOutCount` |
| `item.newCount` |
| `getStockListFactory.count` |
| `downloadIndex` |
| `pageSize` |
| `getStockListFactory.items.length` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `setCustomer(null)` |
| `setCustomer(1)` |
| `setCustomer(2)` |
| `searchStock()` |
| `setStatus(0)` |
| `setStatus(1)` |
| `downloadModal=true` |
| `chooseCategory(` |
| `chooseCategory(item.root.id,false)` |
| `chooseCategoryId(iten.root.id,$event)` |
| `schoolListFactory.nextPage()` |
| `saveInventory()` |
| `downloadModal=false` |
| `daochu()` |

**跳转到**：`goods.materialCompanyInventory`, `materialInventory`

**下拉数据源（ng-options）**

```
x.id as x.name for x in storehouseArr
```

### 3.6 `addMultiDelivery`

- **URL**：`/addMultiDelivery?storehouseId`
- **模板**：`views/materialAdmin/addMultiDelivery.html`
- **控制器**：`addMultiDeliveryCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createStockOutBatchFileTask` | `POST /admin/createStockOutBatchFileTask.json` |
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getCategoryTree2Level` | `POST /admin/getCategoryTree2Level.json` |
| `getProductSkuInVoList` | `POST /admin/getProductSkuInVoList.json` |
| `getStorehouseVo` | `POST /admin/getStorehouseVo.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 剩余数量 |
| 6 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.brandId` |
| `obj.keyword` |
| `pageSize` |
| `obj.model1Keyword` |
| `obj.model2Keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getSupplierListFactory.count` |
| `getStoreNameFactory.result.object.storehouse.name` |
| `province.id` |
| `province.brandName` |
| `item.root.categoryName` |
| `iten.root.categoryName` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockInSkuExistCount` |
| `item.unLockExistSkuCount` |
| `data.filepath` |
| `downloadIndex` |
| `pageSize` |
| `getSupplierListFactory.items.length` |

**页面动作（ng-click）**

| 动作 |
|---|
| `outPort()` |
| `multiOutPort()` |
| `chooseCategory(` |
| `chooseCategory(item.root.id,false)` |
| `chooseCategoryId(iten.root.id,$event)` |
| `createTask()` |
| `importModal=false` |
| `downloadModal=false` |
| `daochu()` |

**跳转到**：`goods.materialCompanyDelivery`, `materialDelivery`

### 3.7 `goods.addCompanyMultiDelivery`

- **URL**：`/addCompanyMultiDelivery?storehouseId`
- **模板**：`views/materialAdmin/addMultiDelivery.html`
- **控制器**：`addMultiDeliveryCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createStockOutBatchFileTask` | `POST /admin/createStockOutBatchFileTask.json` |
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getCategoryTree2Level` | `POST /admin/getCategoryTree2Level.json` |
| `getProductSkuInVoList` | `POST /admin/getProductSkuInVoList.json` |
| `getStorehouseVo` | `POST /admin/getStorehouseVo.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 剩余数量 |
| 6 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.brandId` |
| `obj.keyword` |
| `pageSize` |
| `obj.model1Keyword` |
| `obj.model2Keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getSupplierListFactory.count` |
| `getStoreNameFactory.result.object.storehouse.name` |
| `province.id` |
| `province.brandName` |
| `item.root.categoryName` |
| `iten.root.categoryName` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockInSkuExistCount` |
| `item.unLockExistSkuCount` |
| `data.filepath` |
| `downloadIndex` |
| `pageSize` |
| `getSupplierListFactory.items.length` |

**页面动作（ng-click）**

| 动作 |
|---|
| `outPort()` |
| `multiOutPort()` |
| `chooseCategory(` |
| `chooseCategory(item.root.id,false)` |
| `chooseCategoryId(iten.root.id,$event)` |
| `createTask()` |
| `importModal=false` |
| `downloadModal=false` |
| `daochu()` |

**跳转到**：`goods.materialCompanyDelivery`, `materialDelivery`

### 3.8 `addMultiReceipts`

- **URL**：`/addMultiReceipts`
- **模板**：`views/materialAdmin/addMultiReceipts.html`
- **控制器**：`addMultiReceiptsCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createStockInBatchFileTask` | `POST /admin/createStockInBatchFileTask.json` |
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getCategoryTree2Level` | `POST /admin/getCategoryTree2Level.json` |
| `getProductSkuVoList` | `POST /admin/getProductSkuVoList.json` |
| `getStorehouseVo` | `POST /admin/getStorehouseVo.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表单标签**

| 标签 |
|---|
| {{item.storehouse.name}} |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.model1Keyword` |
| `obj.model2Keyword` |
| `obj.brandId` |
| `pageSize` |
| `store.storehouseId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getSupplierListFactory.count` |
| `getStoreNameFactory.result.object.storehouse.name` |
| `province.id` |
| `province.brandName` |
| `item.root.categoryName` |
| `iten.root.categoryName` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `data.filepath` |
| `item.storehouse.id` |
| `item.storehouse.name` |
| `downloadIndex` |
| `pageSize` |
| `getSupplierListFactory.items.length` |

**页面动作（ng-click）**

| 动作 |
|---|
| `downloadModal=true` |
| `importModal=true` |
| `chooseCategory(` |
| `chooseCategory(item.root.id,false)` |
| `chooseCategoryId(iten.root.id,$event)` |
| `createTask()` |
| `getStoreListFactory.nextPage()` |
| `importModal=false` |
| `downloadModal=false` |
| `daochu()` |

**跳转到**：`goods.companyMaterialReceipts`, `materialImportRecord`, `materialReceipts`

### 3.9 `goods.addCompanyMultiReceipts`

- **URL**：`/addCompanyMultiReceipts?storehouseId`
- **模板**：`views/materialAdmin/addMultiReceipts.html`
- **控制器**：`addMultiReceiptsCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createStockInBatchFileTask` | `POST /admin/createStockInBatchFileTask.json` |
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getCategoryTree2Level` | `POST /admin/getCategoryTree2Level.json` |
| `getProductSkuVoList` | `POST /admin/getProductSkuVoList.json` |
| `getStorehouseVo` | `POST /admin/getStorehouseVo.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表单标签**

| 标签 |
|---|
| {{item.storehouse.name}} |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.model1Keyword` |
| `obj.model2Keyword` |
| `obj.brandId` |
| `pageSize` |
| `store.storehouseId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getSupplierListFactory.count` |
| `getStoreNameFactory.result.object.storehouse.name` |
| `province.id` |
| `province.brandName` |
| `item.root.categoryName` |
| `iten.root.categoryName` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `data.filepath` |
| `item.storehouse.id` |
| `item.storehouse.name` |
| `downloadIndex` |
| `pageSize` |
| `getSupplierListFactory.items.length` |

**页面动作（ng-click）**

| 动作 |
|---|
| `downloadModal=true` |
| `importModal=true` |
| `chooseCategory(` |
| `chooseCategory(item.root.id,false)` |
| `chooseCategoryId(iten.root.id,$event)` |
| `createTask()` |
| `getStoreListFactory.nextPage()` |
| `importModal=false` |
| `downloadModal=false` |
| `daochu()` |

**跳转到**：`goods.companyMaterialReceipts`, `materialImportRecord`, `materialReceipts`

### 3.10 `goods.addProductBivariateTable`

- **URL**：`/addProductBivariateTable?storehouseId&productId`
- **模板**：`views/materialAdmin/addProductBivariateTable.html`
- **控制器**：`addProductBivariateTableCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createStockTakingByProductSku` | `POST /admin/createStockTakingByProductSku.json` |
| `getStockCountForTwoDimensionalTable` | `POST /admin/getStockCountForTwoDimensionalTable.json` |
| `getStorehouseVo` | `POST /admin/getStorehouseVo.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表单标签**

| 标签 |
|---|
| 库存小于0 |
| 库存等于0 |
| 库存大于0 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{getList.result.object.product[direction.xName]}} {{getList.result.object.product[direction.yName]}} |
| 2 | {{col}} |
| 3 | {{row}} |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `model.model1Keyword` |
| `model.model2Keyword` |
| `model.skuCodeKeyword` |
| `obj.lessThanZero` |
| `obj.equalToZero` |
| `obj.moreThanZero` |
| `iten.stockInSkuExistCount2` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `storeName` |
| `getList.result.object.product.productName` |
| `getList.result.object.product.model1Name` |
| `getList.result.object.product.model2Name` |
| `getList.result.object.product` |
| `direction.xName` |
| `direction.yName` |
| `col` |
| `row` |
| `iten.id` |
| `iten.stockInSkuExistCounts` |

**页面动作（ng-click）**

| 动作 |
|---|
| `getEr()` |
| `saveInventory()` |

**跳转到**：`goods.materialCompanyInventory`

### 3.11 `goods.addProductDelivery`

- **URL**：`/addProductDelivery?storehouseId&productType`
- **模板**：`views/materialAdmin/addProductDelivery.html`
- **控制器**：`addProductDeliveryCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createStockOutByProductSku` | `POST /admin/createStockOutByProductSku.json` |
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getProductSkuInVoList` | `POST /admin/getProductSkuInVoList.json` |
| `getStorehouseVo` | `POST /admin/getStorehouseVo.json` |
| `selectEmployeeByName` | `POST /admin/selectEmployeeByName.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 出库数量 |
| 7 | 成本价(￥) |
| 8 | 有效期 |
| 9 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `create.outDate` |
| `create.outType` |
| `supplierKeyword` |
| `item.outCount` |
| `obj.storehouseId` |
| `obj.remark` |
| `create.remark` |
| `obj.keyword` |
| `obj.modelKeyword` |
| `obj.brandId` |
| `product.productSku` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `create.outDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `supplierWord` |
| `item.employeeName` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `item.model1Name` |
| `item.model1` |
| `item.model2Name` |
| `item.model2` |
| `item.unLockExistSkuCount` |
| `totalprice` |
| `outCount` |
| `storeName` |
| `province.id` |
| `province.brandName` |
| `item.product.productName` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `open1()` |
| `showsupplierList($event)` |
| `searchSupplierList(supplierKeyword,$event)` |
| `selectSupplier(item.id,item.employeeName)` |
| `clearSupplier()` |
| `showInfo(item)` |
| `deleteReceipt($index)` |
| `showAddModal()` |
| `addDelivery()` |
| `selectProductName(item.productSku.id,$index)` |
| `getProductListFactory.nextPage()` |
| `selectProduct()` |
| `hideProductModal()` |

**跳转到**：`goods.materialCompanyDelivery`, `materialDelivery`

**下拉数据源（ng-options）**

```
x.id as x.name for x in outType
x.id as x.name for x in storehouseArr
```

### 3.12 `goods.addProductInventory`

- **URL**：`/addProductInventory?storehouseId`
- **模板**：`views/materialAdmin/addProductInventory.html`
- **控制器**：`addProductInventoryCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createStockTakingByProductSku` | `POST /admin/createStockTakingByProductSku.json` |
| `getCategoryTree2Level` | `POST /admin/getCategoryTree2Level.json` |
| `getProductSkuInVoList` | `POST /admin/getProductSkuInVoList.json` |
| `getStorehouseVo` | `POST /admin/getStorehouseVo.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表单标签**

| 标签 |
|---|
| 库存小于0 |
| 库存等于0 |
| 库存大于0 |
| 正常 |
| 停用 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 品牌/类目 |
| 2 | 商品信息 |
| 3 | 规格 |
| 4 | 账面数量 |
| 5 | 实际数量 |
| 6 | 盘盈盘亏 |
| 7 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.storehouseId` |
| `obj.lessThanZero` |
| `obj.equalToZero` |
| `obj.moreThanZero` |
| `item.newCount` |
| `pageSize` |
| `obj.keyword` |
| `obj.modelKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `storeName` |
| `item.root.categoryName` |
| `iten.root.categoryName` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockInSkuExistCount` |
| `item.newCount` |
| `getStockListFactory.count` |
| `downloadIndex` |
| `pageSize` |
| `getStockListFactory.items.length` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `setCustomer(null)` |
| `setCustomer(1)` |
| `setCustomer(2)` |
| `downloadModal=true` |
| `searchStock()` |
| `setStatus(0)` |
| `setStatus(1)` |
| `chooseCategory(` |
| `chooseCategory(item.root.id,false)` |
| `chooseCategoryId(iten.root.id,$event)` |
| `schoolListFactory.nextPage()` |
| `openBivariate(item)` |
| `saveInventory()` |
| `downloadModal=false` |
| `daochu()` |

**跳转到**：`goods.materialCompanyInventory`, `materialInventory`

**下拉数据源（ng-options）**

```
x.id as x.name for x in storehouseArr
```

### 3.13 `addPurchaseRequest`

- **URL**：`/addPurchaseRequest`
- **模板**：`views/materialAdmin/addPurchaseRequest.html`
- **控制器**：`addPurchaseRequestCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 剩余数量 |
| 6 | 采购数量 |
| 7 | 序号 |
| 8 | 品牌/类目 |
| 9 | 商品信息 |
| 10 | 规格 |
| 11 | 采购数量 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.brandId` |
| `obj.keyword` |
| `item.skuCount` |
| `pageSize` |
| `purchase.requestTime` |
| `purchase.remark` |
| `item.purchaseRequestSku.skuCount` |
| `tab.count` |
| `tab.purchaseCount` |
| `obj.model1Keyword` |
| `obj.model2Keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `province.id` |
| `province.brandName` |
| `item.root.categoryName` |
| `iten.root.categoryName` |
| `index` |
| `getStockListFactory.index` |
| `pageSize` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockInSkuExistCount` |
| `totalCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `chooseCategory(` |
| `chooseCategory(item.root.id,false)` |
| `chooseCategoryId(iten.root.id,$event)` |
| `schoolListFactory.nextPage()` |
| `setTab()` |
| `open1()` |
| `addPurchase()` |
| `preview()` |
| `setCountTab()` |
| `selectProduct()` |
| `hideProductModal()` |
| `setAllProduct(tab.count)` |
| `setAllModal=false` |
| `setProduct(tab.purchaseCount)` |
| `setModal=false` |

**跳转到**：`materialPurchaseRequest`

### 3.14 `purchase.addPurchasement`

- **URL**：`/addPurchasement`
- **模板**：`views/materialAdmin/addPurchasement.html`
- **控制器**：`addPurchasementCtrl`
- **端点数**：8

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createPurchaseRequestAndSkuList` | `POST /admin/createPurchaseRequestAndSkuList.json` |
| `createStockPurchaseAndSkuList` | `POST /admin/createStockPurchaseAndSkuList.json` |
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getCategoryTree2Level` | `POST /admin/getCategoryTree2Level.json` |
| `getProductSkuExistCountVoList` | `POST /admin/getProductSkuExistCountVoList.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |
| `viewPurchaseRequestSkuVoList` | `POST /admin/viewPurchaseRequestSkuVoList.json` |
| `viewStockPurchaseSkuVoList` | `POST /admin/viewStockPurchaseSkuVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品规格信息 |
| 4 | 剩余数量 |
| 5 | 采购数量 |
| 6 | 供应商 |
| 7 | 序号 |
| 8 | 品牌/类目 |
| 9 | 商品规格信息 |
| 10 | 采购数量 |
| 11 | 小计 |
| 12 | 供应商 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.brandId` |
| `obj.keyword` |
| `obj.model1Keyword` |
| `obj.model2Keyword` |
| `obj.storehouseId` |
| `item.skuCount` |
| `pageSize` |
| `purchase.purchaseDate` |
| `purchase.purchaser` |
| `purchase.remark` |
| `item.stockPurchaseSku.skuCount` |
| `tab.count` |
| `tab.purchaseCount` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `province.id` |
| `province.brandName` |
| `item.root.categoryName` |
| `iten.root.categoryName` |
| `index` |
| `getStockListFactory.index` |
| `pageSize` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.productSku.model1` |
| `item.productSku.model2` |
| `item.product.factory` |
| `item.productSku.costPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.stockInSkuExistCount` |
| `len` |
| `orderLength` |
| `item.supplier.supplierName` |
| `totalCountPrice` |
| `toFixed` |
| `totalCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `chooseCategory(` |
| `chooseCategory(item.root.id,false)` |
| `chooseCategoryId(iten.root.id,$event)` |
| `schoolListFactory.nextPage()` |
| `setTab()` |
| `open1()` |
| `makePurchase()` |
| `preview()` |
| `addPurchase()` |
| `$close()` |
| `setCountTab()` |
| `selectProduct()` |
| `hideProductModal()` |
| `setAllProduct(tab.count)` |
| `setAllModal=false` |
| `setProduct(tab.purchaseCount)` |
| `setModal=false` |

**跳转到**：`purchase.materialPurchase`

**下拉数据源（ng-options）**

```
x.id as x.name for x in storehouseArr
```

### 3.15 `goods.addCompanyReceipt`

- **URL**：`/addCompanyReceipt?storehouseId`
- **模板**：`views/materialAdmin/addReceipt.html`
- **控制器**：`addReceiptCtrl`
- **端点数**：7

**调用的端点**

| 动作 | 端点 |
|---|---|
| `changeToProductSkuVoList` | `POST /admin/changeToProductSkuVoList.json` |
| `createStockInAndSkuList` | `POST /admin/createStockInAndSkuList.json` |
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getProductSkuPlaneVo` | `POST /admin/getProductSkuPlaneVo.json` |
| `getProductVoList` | `POST /admin/getProductVoList.json` |
| `getStorehouseVo` | `POST /admin/getStorehouseVo.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 生产厂家 |
| 6 | 生产许可证号 |
| 7 | 数量 |
| 8 | 批号 |
| 9 | 生产日期 |
| 10 | 有效期 |
| 11 | 唯一标识码 |
| 12 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.inDate` |
| `obj.inType` |
| `item.skuCount` |
| `item.batchNo` |
| `item.productionDate` |
| `item.expiresDate` |
| `obj.storehouseId` |
| `obj.remark` |
| `productword` |
| `model1Keyword` |
| `model2Keyword` |
| `skuCodeKeyword` |
| `productcount` |
| `tab.amount` |
| `tab.batchNo` |
| `tab.time` |
| `tab.time2` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.inDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `item.model1Name` |
| `item.model1` |
| `item.model2Name` |
| `item.model2` |
| `item.factoryLicense` |
| `item.uniqueCode` |
| `totalprice` |
| `storeName` |
| `productkeyword` |
| `item.product.productName` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.factory` |
| `item.product.productCode` |
| `getPlaneFactory.result.object.product.model1Name` |
| `getPlaneFactory.result.object.product.model2Name` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `open1()` |
| `bindUdi.setShow(true)` |
| `bindUdi.allChoseFun()` |
| `setTab(1)` |
| `setTab(2)` |
| `setTab(4)` |
| `setTab(3)` |
| `bindUdi.choseSingle(item)` |
| `deleteReceipt($index)` |
| `showAddModal()` |
| `addReceipt()` |
| `supplierList=false` |
| `showsupplierList($event)` |
| `searchProductList(productword,$event)` |
| `setProduct(item.product.productName,item.product.id)` |
| `searchName()` |
| `affrim()` |
| `hideProductModal()` |
| `selectProduct()` |
| `setCount()` |
| `setCountModal=false` |
| `open2()` |
| `setAllProduct()` |
| `setAllModal=false` |

**跳转到**：`goods.companyMaterialReceipts`, `materialReceipts`

**下拉数据源（ng-options）**

```
x.id as x.name for x in inType
x.id as x.name for x in storehouseArr
```

### 3.16 `addReceipt`

- **URL**：`/addReceipt`
- **模板**：`views/materialAdmin/addReceipt.html`
- **控制器**：`addReceiptCtrl`
- **端点数**：7

**调用的端点**

| 动作 | 端点 |
|---|---|
| `changeToProductSkuVoList` | `POST /admin/changeToProductSkuVoList.json` |
| `createStockInAndSkuList` | `POST /admin/createStockInAndSkuList.json` |
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getProductSkuPlaneVo` | `POST /admin/getProductSkuPlaneVo.json` |
| `getProductVoList` | `POST /admin/getProductVoList.json` |
| `getStorehouseVo` | `POST /admin/getStorehouseVo.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 生产厂家 |
| 6 | 生产许可证号 |
| 7 | 数量 |
| 8 | 批号 |
| 9 | 生产日期 |
| 10 | 有效期 |
| 11 | 唯一标识码 |
| 12 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.inDate` |
| `obj.inType` |
| `item.skuCount` |
| `item.batchNo` |
| `item.productionDate` |
| `item.expiresDate` |
| `obj.storehouseId` |
| `obj.remark` |
| `productword` |
| `model1Keyword` |
| `model2Keyword` |
| `skuCodeKeyword` |
| `productcount` |
| `tab.amount` |
| `tab.batchNo` |
| `tab.time` |
| `tab.time2` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.inDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `item.model1Name` |
| `item.model1` |
| `item.model2Name` |
| `item.model2` |
| `item.factoryLicense` |
| `item.uniqueCode` |
| `totalprice` |
| `storeName` |
| `productkeyword` |
| `item.product.productName` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.factory` |
| `item.product.productCode` |
| `getPlaneFactory.result.object.product.model1Name` |
| `getPlaneFactory.result.object.product.model2Name` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `open1()` |
| `bindUdi.setShow(true)` |
| `bindUdi.allChoseFun()` |
| `setTab(1)` |
| `setTab(2)` |
| `setTab(4)` |
| `setTab(3)` |
| `bindUdi.choseSingle(item)` |
| `deleteReceipt($index)` |
| `showAddModal()` |
| `addReceipt()` |
| `supplierList=false` |
| `showsupplierList($event)` |
| `searchProductList(productword,$event)` |
| `setProduct(item.product.productName,item.product.id)` |
| `searchName()` |
| `affrim()` |
| `hideProductModal()` |
| `selectProduct()` |
| `setCount()` |
| `setCountModal=false` |
| `open2()` |
| `setAllProduct()` |
| `setAllModal=false` |

**跳转到**：`goods.companyMaterialReceipts`, `materialReceipts`

**下拉数据源（ng-options）**

```
x.id as x.name for x in inType
x.id as x.name for x in storehouseArr
```

### 3.17 `purchase.addSalePurchase`

- **URL**：`/addSalePurchase`
- **模板**：`views/materialAdmin/addSalePurchase.html`
- **控制器**：`addSalePurchaseCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createStockPurchaseAndSkuList` | `POST /admin/createStockPurchaseAndSkuList.json` |
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getCategoryTree2Level` | `POST /admin/getCategoryTree2Level.json` |
| `selectMedicalProductSkuUseVoList` | `POST /admin/selectMedicalProductSkuUseVoList.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |
| `viewStockPurchaseSkuVoList` | `POST /admin/viewStockPurchaseSkuVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品规格信息 |
| 4 | 本期销量 |
| 5 | 采购数量 |
| 6 | 供应商 |
| 7 | 序号 |
| 8 | 品牌/类目 |
| 9 | 商品规格信息 |
| 10 | 采购数量 |
| 11 | 小计 |
| 12 | 供应商 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `obj.rightTimer` |
| `dateSearch` |
| `obj.brandId` |
| `obj.keyword` |
| `obj.modelKeyword` |
| `obj.storehouseId` |
| `item.skuCount` |
| `pageSize` |
| `purchase.purchaseDate` |
| `purchase.purchaser` |
| `purchase.remark` |
| `item.stockPurchaseSku.skuCount` |
| `tab.count` |
| `tab.purchaseCount` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `province.id` |
| `province.brandName` |
| `item.root.categoryName` |
| `iten.root.categoryName` |
| `index` |
| `getStockListFactory.index` |
| `pageSize` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.productSku.model1` |
| `item.productSku.model2` |
| `item.product.factory` |
| `item.productSku.costPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.medicalProductSkuUseData.useCount` |
| `len` |
| `orderLength` |
| `item.supplier.supplierName` |
| `totalCountPrice` |
| `toFixed` |
| `totalCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `searchDate()` |
| `chooseCategory(` |
| `chooseCategory(item.root.id,false)` |
| `chooseCategoryId(iten.root.id,$event)` |
| `schoolListFactory.nextPage()` |
| `setToCount()` |
| `setTab()` |
| `open3()` |
| `makePurchase()` |
| `preview()` |
| `addPurchase()` |
| `$close()` |
| `setCountTab()` |
| `selectProduct()` |
| `hideProductModal()` |
| `setAllProduct(tab.count)` |
| `setAllModal=false` |
| `setToProduct()` |
| `setToModal=false` |
| `setProduct(tab.purchaseCount)` |
| `setModal=false` |

**跳转到**：`purchase.materialPurchase`

**下拉数据源（ng-options）**

```
x.id as x.name for x in storehouseArr
```

### 3.18 `addStockChange`

- **URL**：`/addStockChange`
- **模板**：`views/materialAdmin/addStockChange.html`
- **控制器**：`addStockChangeCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createStockTransferAndSkuList` | `POST /admin/createStockTransferAndSkuList.json` |
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getProductSkuInVoList` | `POST /admin/getProductSkuInVoList.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 |
| 6 | 出库数量 |
| 7 | 成本价(￥) |
| 8 | 批次 |
| 9 | 有效期 |
| 10 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.outStorehouseId` |
| `obj.inStorehouseId` |
| `obj.outDate` |
| `item.outCount` |
| `obj.operator` |
| `obj.remark` |
| `stock.keyword` |
| `stock.modelKeyword` |
| `product.productSku` |
| `stock.brandId` |
| `select.stockInSkuId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `modelName.id` |
| `modelName.name` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `item.model1Name` |
| `item.model1` |
| `item.model2` |
| `item.unLockExistSkuCount` |
| `item.batchNo` |
| `item.expiresDateLong` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.product.productName` |
| `item.productSku.model2` |
| `item.productSku.model1` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `province.id` |
| `province.brandName` |
| `getProductListFactory.items` |
| `select.idx` |
| `unLockExistSkuCount` |
| `iten.unLockExistSkuCount` |
| `iten.stockIn.inDate` |
| `iten.storehouse.name` |
| `iten.stockInSku.expiresDate` |
| `iten.stockInSku.batchNo` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `open1()` |
| `deleteReceipt($index)` |
| `showAddModal()` |
| `addDelivery()` |
| `selectProductName(item.productSku.id,$index)` |
| `getProductListFactory.nextPage()` |
| `setstockInSkuId(iten.stockInSku.id,$index)` |
| `selectProduct()` |
| `hideProductModal()` |

**跳转到**：`goods.stockCompanyChange`, `stockChange`

### 3.19 `goods.addStockCompanyChange`

- **URL**：`/addStockCompanyChange?storehouseId&status`
- **模板**：`views/materialAdmin/addStockCompanyChange.html`
- **控制器**：`addStockChangeCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createStockTransferAndSkuList` | `POST /admin/createStockTransferAndSkuList.json` |
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getProductSkuInVoList` | `POST /admin/getProductSkuInVoList.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 出库数量 |
| 7 | 成本价(￥) |
| 8 | 生产日期 |
| 9 | 批号 |
| 10 | 有效期 |
| 11 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.outStorehouseId` |
| `obj.inStorehouseId` |
| `obj.outDate` |
| `item.outCount` |
| `obj.operator` |
| `obj.remark` |
| `stock.keyword` |
| `stock.modelKeyword` |
| `product.productSku` |
| `stock.brandId` |
| `select.stockInSkuId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `modelName.id` |
| `modelName.name` |
| `obj.outDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `item.model1Name` |
| `item.model1` |
| `item.model2` |
| `item.unLockExistSkuCount` |
| `item.productionDateLong` |
| `item.batchNo` |
| `item.expiresDateLong` |
| `totalprice` |
| `outCount` |
| `item.product.productName` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `province.id` |
| `province.brandName` |
| `getProductListFactory.items` |
| `select.idx` |
| `unLockExistSkuCount` |
| `iten.unLockExistSkuCount` |
| `iten.stockIn.inDate` |
| `iten.storehouse.name` |
| `iten.stockInSku.productionDate` |
| `iten.stockInSku.expiresDate` |
| `iten.stockInSku.batchNo` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `open1()` |
| `deleteReceipt($index)` |
| `showAddModal()` |
| `addDelivery()` |
| `selectProductName(item.productSku.id,$index)` |
| `getProductListFactory.nextPage()` |
| `setstockInSkuId(iten.stockInSku.id,$index)` |
| `selectProduct()` |
| `hideProductModal()` |

**跳转到**：`goods.stockCompanyChange`, `stockChange`

### 3.20 `goods.addStockProductChange`

- **URL**：`/addStockProductChange?storehouseId&status`
- **模板**：`views/materialAdmin/addStockProductChange.html`
- **控制器**：`addStockProductChangeCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createStockTransferByProductSku` | `POST /admin/createStockTransferByProductSku.json` |
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getProductSkuInVoList` | `POST /admin/getProductSkuInVoList.json` |
| `getStockTransferVo` | `POST /admin/getStockTransferVo.json` |
| `selectSettlementBySupplier` | `POST /admin/selectSettlementBySupplier.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 出库数量 |
| 7 | 成本价(￥) |
| 8 | 有效期 |
| 9 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.outStorehouseId` |
| `obj.inStorehouseId` |
| `obj.outDate` |
| `item.outCount` |
| `obj.operator` |
| `obj.remark` |
| `stock.keyword` |
| `stock.modelKeyword` |
| `stock.brandId` |
| `product.productSku` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `modelName.id` |
| `modelName.name` |
| `obj.outDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `item.model1Name` |
| `item.model1` |
| `item.model2Name` |
| `item.model2` |
| `item.unLockExistSkuCount` |
| `totalprice` |
| `outCount` |
| `province.id` |
| `province.brandName` |
| `item.product.productName` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `open1()` |
| `deleteReceipt($index)` |
| `showAddModal()` |
| `addDelivery()` |
| `selectProductName(item.productSku.id,$index)` |
| `getProductListFactory.nextPage()` |
| `selectProduct()` |
| `hideProductModal()` |

**跳转到**：`goods.stockCompanyChange`, `stockChange`

### 3.21 `adminBill`

- **URL**：`/adminBill`
- **模板**：`views/materialAdmin/adminBill.html`
- **控制器**：`adminBillCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 供应商 |
| 3 | 期初欠款（元） |
| 4 | 本期应付（元） |
| 5 | 本期付款（元） |
| 6 | 本期退货（元） |
| 7 | 期末欠缴（元） |
| 8 | 操作 |
| 9 | 供应商 |
| 10 | 初期欠款（元） |
| 11 | 本期应付（元） |
| 12 | 本期付款（元） |
| 13 | 本期退货（元） |
| 14 | 期末欠款（元） |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `rightTime` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `resultObj.lookdMsg.total.initialDebet` |
| `outPutDollars` |
| `resultObj.lookdMsg.total.totalInPrice` |
| `resultObj.lookdMsg.total.totalPayment` |
| `resultObj.lookdMsg.total.totalOutPrice` |
| `resultObj.lookdMsg.total.endingDebet` |
| `index` |
| `item.supplier.supplierName` |
| `item.settlementVo.initialDebet` |
| `item.settlementVo.totalInPrice` |
| `item.settlementVo.totalPayment` |
| `item.settlementVo.totalOutPrice` |
| `item.settlementVo.endingDebet` |
| `companyFactory.object.logo` |
| `obj.startTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `rightTime` |
| `companyFactory.object.corporationName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `printList()` |
| `daochu()` |

### 3.22 `adminBillDetial`

- **URL**：`/adminBillDetial?supplierId`
- **模板**：`views/materialAdmin/adminBillDetial.html`
- **控制器**：`adminBillDetialCtrl`
- **端点数**：10

**调用的端点**

| 动作 | 端点 |
|---|---|
| `cancelStockOutForPurchaseOut` | `POST /admin/cancelStockOutForPurchaseOut.json` |
| `completeSupplierSettlement` | `POST /admin/completeSupplierSettlement.json` |
| `completeSupplierSettlementBack` | `POST /admin/completeSupplierSettlementBack.json` |
| `createStockSettlementFromTranferOrBack` | `POST /admin/createStockSettlementFromTranferOrBack.json` |
| `getStockOutVo` | `POST /admin/getStockOutVo.json` |
| `getStockSettlementVoDetail` | `POST /admin/getStockSettlementVoDetail.json` |
| `getSupplier` | `POST /admin/getSupplier.json` |
| `getUnPaymentOfStockSettlement` | `POST /admin/getUnPaymentOfStockSettlement.json` |
| `selectStockSettlementVoList` | `POST /admin/selectStockSettlementVoList.json` |
| `verifySettlement` | `POST /admin/verifySettlement.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 供应商： |
| 2 | {{supplierName}} |
| 3 | 序号 |
| 4 | 费用类型 |
| 5 | 单号 |
| 6 | 制单日期 |
| 7 | 单据金额（元） |
| 8 | 状态 |
| 9 | 备注 |
| 10 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `paramsObj.startTime` |
| `rightTime` |
| `paramsObj.settlementType` |
| `paramsObj.keyword` |
| `jieZhangStatus` |
| `feeParamsObj.settlementType` |
| `feeParamsObj.totalPrice` |
| `feeParamsObj.remark` |
| `msgObj.jieSuanObj.payMoney` |
| `msgObj.jieSuanObj.jieSuanRemark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `supplierName` |
| `resultObj.lookdMsg.total.initialDebet` |
| `outPutDollars` |
| `resultObj.lookdMsg.total.totalInPrice` |
| `resultObj.lookdMsg.total.totalPayment` |
| `resultObj.lookdMsg.total.totalOutPrice` |
| `resultObj.lookdMsg.total.endingDebet` |
| `index` |
| `getBillType` |
| `item.stockSettlement.settlementType` |
| `item.stockSettlement.settlementCode` |
| `item.stockSettlement.settlementDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.stockSettlement.totalPrice` |
| `item.stockSettlement.totalBackPrice` |
| `item.stockSettlement.remark` |
| `msgObj.dialogTitle` |
| `msgObj.jieSuanObj.waitMoney` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `msgObj.addFeeDialogShow = true` |
| `expose()` |
| `sureAddFee()` |
| `closeDialog()` |
| `openSureDialog(item.stockSettlement.id)` |
| `openJieSuanDialog(item.stockSettlement.id,item.stockSettlement.settlementType)` |
| `sureDuiZhang()` |
| `sureJieSuan()` |

**跳转到**：`adminBill`

### 3.23 `adminBillOneDetial`

- **URL**：`/adminBillOneDetial?supplierId&stockSettlementId`
- **模板**：`views/materialAdmin/adminBillOneDetial.html`
- **控制器**：`adminBillOneDetialCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 订货信息 |
| 6 | 入库单价(元) |
| 7 | 入库数量 |
| 8 | 入库金额(元) |
| 9 | 备注 |
| 10 | 序号 |
| 11 | 品牌/类目 |
| 12 | 商品信息 |
| 13 | 规格 |
| 14 | 退货单价(元) |
| 15 | 退货数量 |
| 16 | 退货金额(元) |
| 17 | 备注 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `resultMsg.stockPurchaseInVo.stockPurchaseIn.id` |
| `resultMsg.stockPurchaseInVo.storehouse.name` |
| `resultMsg.stockPurchaseInVo.stockPurchaseIn.createName` |
| `resultMsg.stockPurchaseInVo.stockPurchaseIn.checkName` |
| `resultMsg.stockSettlement.allSettlement` |
| `getType` |
| `resultMsg.stockPurchaseOutVo.stockPurchaseOut.id` |
| `resultMsg.stockPurchaseOutVo.stockPurchaseOut.createName` |
| `resultMsg.stockPurchaseOutVo.storehouse.name` |
| `resultMsg.stockPurchaseOutVo.supplier.supplierName` |
| `resultMsg.stockPurchaseOutVo.stockPurchaseOut.remark` |
| `resultMsg.stockSettlement.id` |
| `resultMsg.stockSettlement.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `HH` |
| `mm` |
| `ss` |
| `resultMsg.stockSettlement.createName` |
| `resultMsg.stockSettlement.remark` |
| `item.payTime` |
| `item.payment` |
| `item.remark` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.factory` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockPurchaseSku.skuPrice` |
| `item.inSkuCount` |
| `item.stockPurchaseSku.remark` |
| `item.stockPurchaseOutSku.outSkuPrice` |
| `item.stockPurchaseOutSku.outCount` |
| `item.stockPurchaseOutSku.outTotalSkuPrice` |
| `ruKuCount` |
| `chuKuCount` |

### 3.24 `deliveryDelete`

- **URL**：`/deliveryDelete?stockOutId`
- **模板**：`views/materialAdmin/deliveryDelete.html`
- **控制器**：`deliveryDeleteCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 出库数量 |
| 7 | 生产日期 |
| 8 | 批号 |
| 9 | 有效期 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.stockOut.id` |
| `obj.stockOut.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `obj.stockOut.createName` |
| `obj.stockOut.outDate` |
| `obj.stockOut.outType` |
| `outType` |
| `obj.drawEmployee.employeeName` |
| `obj.storehouse.name` |
| `obj.stockOut.remark` |
| `obj.stockOut.checkDate` |
| `obj.stockOut.checkName` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.factory` |
| `item.productSku.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockInSku.remark` |
| `item.unLockExistSkuCount` |
| `item.stockOutSku.outCount` |
| `item.stockInSku.productionDate` |
| `item.stockInSku.batchNo` |
| `item.stockInSku.expiresDate` |
| `totalExistCount` |
| `totalprice` |

**页面动作（ng-click）**

| 动作 |
|---|
| `disable()` |

### 3.25 `goods.deliveryCompanyDetail`

- **URL**：`/deliveryCompanyDetail?stockOutId`
- **模板**：`views/materialAdmin/deliveryDetail.html`
- **控制器**：`deliveryDetailCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getStockOutVo` | `POST /admin/getStockOutVo.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 出库数量 |
| 7 | 成本价 |
| 8 | 成本合计 |
| 9 | 生产日期 |
| 10 | 批号 |
| 11 | 有效期 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.stockOut.id` |
| `obj.stockOut.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `obj.stockOut.createName` |
| `obj.stockOut.outDate` |
| `obj.stockOut.outType` |
| `outType` |
| `obj.drawEmployee.employeeName` |
| `obj.storehouse.name` |
| `obj.stockOut.remark` |
| `obj.stockOut.checkDate` |
| `obj.stockOut.checkName` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.factory` |
| `item.productSku.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockInSku.remark` |
| `item.unLockExistSkuCount` |
| `item.stockOutSku.outCount` |
| `item.stockInSku.skuPrice` |
| `toFixed` |
| `item.stockOutSku.outTotalCostPrice` |
| `item.stockInSku.productionDate` |
| `item.stockInSku.batchNo` |
| `item.stockInSku.expiresDate` |
| `totalExistCount` |
| `totalCount` |
| `outTotalCostPrice` |

**跳转到**：`goods.materialCompanyDelivery`, `materialDelivery`

### 3.26 `deliveryDetail`

- **URL**：`/deliveryDetail?stockOutId`
- **模板**：`views/materialAdmin/deliveryDetail.html`
- **控制器**：`deliveryDetailCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getStockOutVo` | `POST /admin/getStockOutVo.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 出库数量 |
| 7 | 成本价 |
| 8 | 成本合计 |
| 9 | 生产日期 |
| 10 | 批号 |
| 11 | 有效期 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.stockOut.id` |
| `obj.stockOut.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `obj.stockOut.createName` |
| `obj.stockOut.outDate` |
| `obj.stockOut.outType` |
| `outType` |
| `obj.drawEmployee.employeeName` |
| `obj.storehouse.name` |
| `obj.stockOut.remark` |
| `obj.stockOut.checkDate` |
| `obj.stockOut.checkName` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.factory` |
| `item.productSku.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockInSku.remark` |
| `item.unLockExistSkuCount` |
| `item.stockOutSku.outCount` |
| `item.stockInSku.skuPrice` |
| `toFixed` |
| `item.stockOutSku.outTotalCostPrice` |
| `item.stockInSku.productionDate` |
| `item.stockInSku.batchNo` |
| `item.stockInSku.expiresDate` |
| `totalExistCount` |
| `totalCount` |
| `outTotalCostPrice` |

**跳转到**：`goods.materialCompanyDelivery`, `materialDelivery`

### 3.27 `deliveryDetailCustomer`

- **URL**：`/deliveryDetailCustomer?stockOutId`
- **模板**：`views/materialAdmin/deliveryDetailCustomer.html`
- **控制器**：`deliveryDetailCtrl`
- **端点数**：1

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getStockOutVo` | `POST /admin/getStockOutVo.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品基本信息 |
| 4 | 参数 |
| 5 | 出库数量 |
| 6 | 批次 |
| 7 | 有效期 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.stockOut.id` |
| `obj.stockOut.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `obj.stockOut.createName` |
| `obj.stockOut.outDate` |
| `obj.stockOut.outType` |
| `outType` |
| `obj.drawEmployee.employeeName` |
| `obj.storehouse.name` |
| `obj.stockOut.remark` |
| `obj.stockOut.checkDate` |
| `obj.stockOut.checkName` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.productSku.model1` |
| `item.productSku.model2` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.factory` |
| `item.productSku.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.stockInSku.remark` |
| `item.stockOutSku.outCount` |
| `item.stockInSku.skuCount` |
| `item.stockInSku.skuOutCount` |
| `item.stockIn.inDate` |
| `item.storehouse.name` |
| `item.stockInSku.expiresDate` |
| `item.stockInSku.batchNo` |
| `totalprice` |

**跳转到**：`materialDeliveryCustomer`

### 3.28 `goods.deliveryCompanyModify`

- **URL**：`/deliveryCompanyModify?stockOutId`
- **模板**：`views/materialAdmin/deliveryModify.html`
- **控制器**：`deliveryModifyCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `checkStockOut` | `POST /admin/checkStockOut.json` |
| `getStockOutVo` | `POST /admin/getStockOutVo.json` |
| `selectEmployeeByName` | `POST /admin/selectEmployeeByName.json` |
| `udpateStockOutAndSkuList` | `POST /admin/udpateStockOutAndSkuList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 出库数量 |
| 7 | 成本价 |
| 8 | 成本合计 |
| 9 | 成本价(￥) |
| 10 | 生产日期 |
| 11 | 批号 |
| 12 | 有效期 |
| 13 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.outDate` |
| `obj.outType` |
| `supplierKeyword` |
| `item.outCount` |
| `obj.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockObjectFactory.object.stockOut.id` |
| `getStockObjectFactory.object.stockOut.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `getStockObjectFactory.object.stockOut.createName` |
| `obj.outDate` |
| `supplierKeyword` |
| `item.employeeName` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.model1Name` |
| `item.model1` |
| `printModel` |
| `item.model2Name` |
| `item.model2` |
| `item.remark` |
| `item.unLockExistSkuCount` |
| `item.skuPrice` |
| `toFixed` |
| `item.outTotalCostPrice` |
| `item.productionDate` |
| `item.batchNo` |
| `item.expiresDate` |
| `totalExistCount` |
| `totalprice` |
| `outTotalCostPrice` |
| `getStockObjectFactory.object.storehouse.name` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `open1()` |
| `showsupplierList($event)` |
| `searchSupplierList(supplierKeyword,$event)` |
| `selectSupplier(item.id,item.employeeName)` |
| `clearSupplier()` |
| `deleteReceipt($index)` |
| `saveDelivery()` |
| `checkSupplier()` |

**跳转到**：`goods.materialCompanyDelivery`, `materialDelivery`

**下拉数据源（ng-options）**

```
x.id as x.name for x in outType
```

### 3.29 `deliveryModify`

- **URL**：`/deliveryModify?stockOutId`
- **模板**：`views/materialAdmin/deliveryModify.html`
- **控制器**：`deliveryModifyCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `checkStockOut` | `POST /admin/checkStockOut.json` |
| `getStockOutVo` | `POST /admin/getStockOutVo.json` |
| `selectEmployeeByName` | `POST /admin/selectEmployeeByName.json` |
| `udpateStockOutAndSkuList` | `POST /admin/udpateStockOutAndSkuList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 出库数量 |
| 7 | 成本价 |
| 8 | 成本合计 |
| 9 | 成本价(￥) |
| 10 | 生产日期 |
| 11 | 批号 |
| 12 | 有效期 |
| 13 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.outDate` |
| `obj.outType` |
| `supplierKeyword` |
| `item.outCount` |
| `obj.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockObjectFactory.object.stockOut.id` |
| `getStockObjectFactory.object.stockOut.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `getStockObjectFactory.object.stockOut.createName` |
| `obj.outDate` |
| `supplierKeyword` |
| `item.employeeName` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.model1Name` |
| `item.model1` |
| `printModel` |
| `item.model2Name` |
| `item.model2` |
| `item.remark` |
| `item.unLockExistSkuCount` |
| `item.skuPrice` |
| `toFixed` |
| `item.outTotalCostPrice` |
| `item.productionDate` |
| `item.batchNo` |
| `item.expiresDate` |
| `totalExistCount` |
| `totalprice` |
| `outTotalCostPrice` |
| `getStockObjectFactory.object.storehouse.name` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `open1()` |
| `showsupplierList($event)` |
| `searchSupplierList(supplierKeyword,$event)` |
| `selectSupplier(item.id,item.employeeName)` |
| `clearSupplier()` |
| `deleteReceipt($index)` |
| `saveDelivery()` |
| `checkSupplier()` |

**跳转到**：`goods.materialCompanyDelivery`, `materialDelivery`

**下拉数据源（ng-options）**

```
x.id as x.name for x in outType
```

### 3.30 `deliveryModifyCustomer`

- **URL**：`/deliveryModifyCustomer?stockOutId`
- **模板**：`views/materialAdmin/deliveryModifyCustomer.html`
- **控制器**：`deliveryModifyCustomerCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品基本信息 |
| 4 | 参数 |
| 5 | 出库数量 |
| 6 | 成本价(￥) |
| 7 | 批次 |
| 8 | 有效期 |
| 9 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.outDate` |
| `obj.outType` |
| `supplierKeyword` |
| `item.outCount` |
| `obj.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockObjectFactory.object.stockOut.id` |
| `getStockObjectFactory.object.stockOut.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `getStockObjectFactory.object.stockOut.createName` |
| `supplierKeyword` |
| `item.employeeName` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.model1` |
| `item.model2` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.remark` |
| `item.skuCount` |
| `item.skuOutCount` |
| `item.inDate` |
| `item.name` |
| `item.expiresDate` |
| `item.batchNo` |
| `totalprice` |
| `getStockObjectFactory.object.storehouse.name` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `open1()` |
| `showsupplierList($event)` |
| `searchSupplierList(supplierKeyword,$event)` |
| `selectSupplier(item.id,item.employeeName)` |
| `clearSupplier()` |
| `deleteReceipt($index)` |
| `saveDelivery()` |
| `checkSupplier()` |

**跳转到**：`materialDeliveryCustomer`

**下拉数据源（ng-options）**

```
x.id as x.name for x in outType
```

### 3.31 `goods.deliveryProductDetail`

- **URL**：`/deliveryProductDetail?stockOutId`
- **模板**：`views/materialAdmin/deliveryProductDetail.html`
- **控制器**：`deliveryProductModifyCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `commitStockOutByProductSku` | `POST /admin/commitStockOutByProductSku.json` |
| `getStockOutProductVoList` | `POST /admin/getStockOutProductVoList.json` |
| `getStockOutVo` | `POST /admin/getStockOutVo.json` |
| `selectEmployeeByName` | `POST /admin/selectEmployeeByName.json` |
| `updateStockOutByProductSku` | `POST /admin/updateStockOutByProductSku.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 出库数量 |
| 7 | 成本合计 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockOutObjectFactory.object.stockOut.id` |
| `getStockOutObjectFactory.object.stockOut.createName` |
| `getStockOutObjectFactory.object.stockOut.outDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `getStockOutObjectFactory.object.stockOut.outType` |
| `outType` |
| `getStockOutObjectFactory.object.drawEmployee.employeeName` |
| `getStockOutObjectFactory.object.storehouse.name` |
| `getStockOutObjectFactory.object.stockOut.remark` |
| `getStockOutObjectFactory.object.stockOut.checkName` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.factory` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.unLockExistSkuCount` |
| `item.stockOutProduct.outCount` |
| `item.stockOutProduct.outTotalCostPrice` |
| `toFixed` |
| `totalExistCount` |
| `totalCount` |
| `outTotalCostPrice` |

**跳转到**：`goods.materialCompanyDelivery`

### 3.32 `goods.deliveryProductModify`

- **URL**：`/deliveryProductModify?stockOutId`
- **模板**：`views/materialAdmin/deliveryProductModify.html`
- **控制器**：`deliveryProductModifyCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `commitStockOutByProductSku` | `POST /admin/commitStockOutByProductSku.json` |
| `getStockOutProductVoList` | `POST /admin/getStockOutProductVoList.json` |
| `getStockOutVo` | `POST /admin/getStockOutVo.json` |
| `selectEmployeeByName` | `POST /admin/selectEmployeeByName.json` |
| `updateStockOutByProductSku` | `POST /admin/updateStockOutByProductSku.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 出库数量 |
| 7 | 成本价(￥) |
| 8 | 有效期 |
| 9 | 成本合计 |
| 10 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.outDate` |
| `obj.outType` |
| `supplierKeyword` |
| `item.stockOutProduct.outCount` |
| `obj.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockOutObjectFactory.object.stockOut.id` |
| `getStockOutObjectFactory.object.stockOut.createName` |
| `obj.outDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `supplierKeyword` |
| `item.employeeName` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.factory` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.unLockExistSkuCount` |
| `item.stockOutProduct.outTotalCostPrice` |
| `toFixed` |
| `totalExistCount` |
| `totalCount` |
| `outTotalCostPrice` |
| `getStockOutObjectFactory.object.storehouse.name` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `open1()` |
| `showsupplierList($event)` |
| `searchSupplierList(supplierKeyword,$event)` |
| `selectSupplier(item.id,item.employeeName)` |
| `clearSupplier()` |
| `deleteReceipt($index)` |
| `saveDelivery()` |
| `checkSupplier()` |

**跳转到**：`goods.materialCompanyDelivery`, `materialDelivery`

**下拉数据源（ng-options）**

```
x.id as x.name for x in outType
```

### 3.33 `goods`

- **URL**：`/goods`
- **模板**：`views/materialAdmin/goods.html`
- **控制器**：`goodsCtrl`
- **端点数**：7

**调用的端点**

| 动作 | 端点 |
|---|---|
| `checkStockTaking` | `POST /admin/checkStockTaking.json` |
| `commitStockTakingByProductSku` | `POST /admin/commitStockTakingByProductSku.json` |
| `getChildrenLinkAndCode` | `POST /admin/getChildrenLinkAndCode.json` |
| `getStockTakingProductVoList` | `POST /admin/getStockTakingProductVoList.json` |
| `getStockTakingVo` | `POST /admin/getStockTakingVo.json` |
| `updateStockTakingAndSkuList` | `POST /admin/updateStockTakingAndSkuList.json` |
| `updateStockTakingByProductSku` | `POST /admin/updateStockTakingByProductSku.json` |

### 3.34 `inventoryDetail`

- **URL**：`/inventoryDetail?stockTakingId`
- **模板**：`views/materialAdmin/inventoryDetail.html`
- **控制器**：`inventoryDetailCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 生产日期 |
| 6 | 批次 |
| 7 | 账面数量 |
| 8 | 实际数量 |
| 9 | 盘盈盘亏 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockTakingObjectFactory.object.storehouse.name` |
| `getStockTakingObjectFactory.object.stockTaking.takingDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `getStockTakingObjectFactory.object.stockTaking.createName` |
| `getStockTakingObjectFactory.object.stockTaking.checkDate` |
| `getStockTakingObjectFactory.object.stockTaking.checkName` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockInSku.remark` |
| `item.stockInSku.productionDate` |
| `item.stockIn.gmtCreate` |
| `item.storehouse.name` |
| `item.stockInSku.expiresDate` |
| `item.supplier.supplierName` |
| `item.stockInSku.batchNo` |
| `item.stockTakingSku.oldCount` |
| `item.stockTakingSku.newCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |

**跳转到**：`goods.materialCompanyInventory`, `materialInventory`

### 3.35 `goods.inventoryCompanyDetail`

- **URL**：`/inventoryCompanyDetail?stockTakingId`
- **模板**：`views/materialAdmin/inventoryDetail.html`
- **控制器**：`inventoryDetailCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 生产日期 |
| 6 | 批次 |
| 7 | 账面数量 |
| 8 | 实际数量 |
| 9 | 盘盈盘亏 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockTakingObjectFactory.object.storehouse.name` |
| `getStockTakingObjectFactory.object.stockTaking.takingDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `getStockTakingObjectFactory.object.stockTaking.createName` |
| `getStockTakingObjectFactory.object.stockTaking.checkDate` |
| `getStockTakingObjectFactory.object.stockTaking.checkName` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockInSku.remark` |
| `item.stockInSku.productionDate` |
| `item.stockIn.gmtCreate` |
| `item.storehouse.name` |
| `item.stockInSku.expiresDate` |
| `item.supplier.supplierName` |
| `item.stockInSku.batchNo` |
| `item.stockTakingSku.oldCount` |
| `item.stockTakingSku.newCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |

**跳转到**：`goods.materialCompanyInventory`, `materialInventory`

### 3.36 `inventoryModify`

- **URL**：`/inventoryModify?stockTakingId`
- **模板**：`views/materialAdmin/inventoryModify.html`
- **控制器**：`inventoryModifyCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| 数量大于0 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 生产日期 |
| 6 | 批次 |
| 7 | 账面数量 |
| 8 | 实际数量 |
| 9 | 盘盈盘亏 |
| 10 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.moreThanZero` |
| `item.stockTakingSku.newCount` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockTakingObjectFactory.object.storehouse.name` |
| `getStockTakingObjectFactory.object.stockTaking.takingDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `getStockTakingObjectFactory.object.stockTaking.createName` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockInSku.remark` |
| `item.stockInSku.productionDate` |
| `item.stockIn.gmtCreate` |
| `item.storehouse.name` |
| `item.stockInSku.expiresDate` |
| `item.supplier.supplierName` |
| `item.stockInSku.batchNo` |
| `item.stockTakingSku.oldCount` |
| `item.stockTakingSku.newCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `searchStock()` |
| `deleteReceipt($index)` |
| `saveInventory()` |
| `checkSupplier()` |

**跳转到**：`goods.materialCompanyInventory`, `materialInventory`

### 3.37 `goods.inventoryCompanyModify`

- **URL**：`/inventoryCompanyModify?stockTakingId`
- **模板**：`views/materialAdmin/inventoryModify.html`
- **控制器**：`inventoryModifyCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| 数量大于0 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 生产日期 |
| 6 | 批次 |
| 7 | 账面数量 |
| 8 | 实际数量 |
| 9 | 盘盈盘亏 |
| 10 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.moreThanZero` |
| `item.stockTakingSku.newCount` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockTakingObjectFactory.object.storehouse.name` |
| `getStockTakingObjectFactory.object.stockTaking.takingDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `getStockTakingObjectFactory.object.stockTaking.createName` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockInSku.remark` |
| `item.stockInSku.productionDate` |
| `item.stockIn.gmtCreate` |
| `item.storehouse.name` |
| `item.stockInSku.expiresDate` |
| `item.supplier.supplierName` |
| `item.stockInSku.batchNo` |
| `item.stockTakingSku.oldCount` |
| `item.stockTakingSku.newCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `searchStock()` |
| `deleteReceipt($index)` |
| `saveInventory()` |
| `checkSupplier()` |

**跳转到**：`goods.materialCompanyInventory`, `materialInventory`

### 3.38 `goods.inventoryProductDetail`

- **URL**：`/inventoryProductDetail?stockTakingId`
- **模板**：`views/materialAdmin/inventoryProductDetail.html`
- **控制器**：`inventoryProductModifyCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 账面数量 |
| 6 | 实际数量 |
| 7 | 盘盈盘亏 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockTakingObjectFactory.object.storehouse.name` |
| `getStockTakingObjectFactory.object.stockTaking.takingDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `getStockTakingObjectFactory.object.stockTaking.createName` |
| `getStockTakingObjectFactory.object.stockTaking.checkDate` |
| `getStockTakingObjectFactory.object.stockTaking.checkName` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockTakingProduct.oldCount` |
| `item.stockTakingProduct.newCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |

**跳转到**：`goods.materialCompanyInventory`

### 3.39 `goods.inventoryProductModify`

- **URL**：`/inventoryProductModify?stockTakingId`
- **模板**：`views/materialAdmin/inventoryProductModify.html`
- **控制器**：`inventoryProductModifyCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| 数量大于0 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 账面数量 |
| 6 | 实际数量 |
| 7 | 盘盈盘亏 |
| 8 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.keyword` |
| `obj.moreThanZero` |
| `item.stockTakingProduct.newCount` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockTakingObjectFactory.object.storehouse.name` |
| `getStockTakingObjectFactory.object.stockTaking.takingDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `getStockTakingObjectFactory.object.stockTaking.createName` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockTakingProduct.oldCount` |
| `item.stockTakingProduct.newCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `searchStock()` |
| `deleteReceipt($index)` |
| `saveInventory()` |
| `checkSupplier()` |

**跳转到**：`goods.materialCompanyInventory`

### 3.40 `materialDelivery`

- **URL**：`/materialDelivery`
- **模板**：`views/materialAdmin/materialDelivery.html`
- **控制器**：`materialDeliveryCtrl`
- **端点数**：14

**调用的端点**

| 动作 | 端点 |
|---|---|
| `deleteStockIn` | `POST /admin/deleteStockIn.json` |
| `deleteStockOut` | `POST /admin/deleteStockOut.json` |
| `deleteStockTaking` | `POST /admin/deleteStockTaking.json` |
| `getCorpInfo` | `POST /admin/getCorpInfo.json` |
| `getStockInVoList` | `POST /admin/getStockInVoList.json` |
| `getStockOutProductVoList` | `POST /admin/getStockOutProductVoList.json` |
| `getStockOutVo` | `POST /admin/getStockOutVo.json` |
| `getStockOutVoList` | `POST /admin/getStockOutVoList.json` |
| `getStockTakingProductVoList` | `POST /admin/getStockTakingProductVoList.json` |
| `getStockTakingVo` | `POST /admin/getStockTakingVo.json` |
| `getStockTakingVoList` | `POST /admin/getStockTakingVoList.json` |
| `getStorehouseVo` | `POST /admin/getStorehouseVo.json` |
| `isAdminRoleStateOK` | `POST /admin/isAdminRoleStateOK.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 出库单号 |
| 2 | 出库日期 |
| 3 | 所属仓库 |
| 4 | 出库方式 |
| 5 | 领用人员 |
| 6 | 制单人 |
| 7 | 状态 |
| 8 | 操作 |
| 9 | 序号 |
| 10 | 名称 |
| 11 | 规格 |
| 12 | 零售价/单位 |
| 13 | 出库数量 |
| 14 | 生产厂商 |
| 15 | 成本价 |
| 16 | 成本合计 |
| 17 | 批号 |
| 18 | 有效期 |
| 19 | 序号 |
| 20 | 名称 |
| 21 | 规格 |
| 22 | 零售价/单位 |
| 23 | 出库数量 |
| 24 | 成本合计 |
| 25 | 生产厂商 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.storehouseId` |
| `obj.outType` |
| `obj.startTime` |
| `rightTime` |
| `obj.id` |
| `obj.keyword` |
| `obj.modelKeyword` |
| `param.storehouseId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `tab` |
| `item.stockOut.id` |
| `item.stockOut.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.storehouse.name` |
| `item.stockOut.outType` |
| `outType` |
| `item.drawEmployee.employeeName` |
| `item.stockOut.createName` |
| `item.stockOut.checked` |
| `supplierChecked` |
| `companyFactory.object.logo` |
| `companyFactory.object.corporationName` |
| `getCashflowObjectFactory.object.stockOut.id` |
| `getCashflowObjectFactory.object.stockOut.gmtCreate` |
| `getCashflowObjectFactory.object.stockOut.createName` |
| `getCashflowObjectFactory.object.stockOut.outDate` |
| `getCashflowObjectFactory.object.stockOut.outType` |
| `getCashflowObjectFactory.object.drawEmployee.employeeName` |
| `getCashflowObjectFactory.object.storehouse.name` |
| `getCashflowObjectFactory.object.stockOut.checkDate` |
| `getCashflowObjectFactory.object.stockOut.checkName` |
| `getCashflowObjectFactory.object.stockOut.remark` |
| `index` |
| `item.product.productName` |
| `item.productSku.model1` |
| `printModel` |
| `item.productSku.model2` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.stockOutSku.outCount` |
| `item.product.factory` |
| `item.stockInSku.skuPrice` |
| `toFixed` |
| `item.stockOutSku.outTotalCostPrice` |
| `item.stockOutSku.batchNo` |
| `item.stockOutSku.expiresDate` |
| `getStockOutObjectFactory.object.stockOut.id` |
| `getStockOutObjectFactory.object.stockOut.gmtCreate` |
| `getStockOutObjectFactory.object.stockOut.createName` |
| `getStockOutObjectFactory.object.stockOut.outDate` |
| `getStockOutObjectFactory.object.stockOut.outType` |
| `getStockOutObjectFactory.object.drawEmployee.employeeName` |
| `getStockOutObjectFactory.object.storehouse.name` |
| `getStockOutObjectFactory.object.stockOut.checkDate` |
| `getStockOutObjectFactory.object.stockOut.checkName` |
| `getStockOutObjectFactory.object.stockOut.remark` |
| `item.stockOutProduct.outCount` |
| `item.stockOutProduct.outTotalCostPrice` |
| `item.storehouse.id` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setProduct(1)` |
| `setProduct(2)` |
| `importModal=true` |
| `selectedStore()` |
| `setCustomer(null)` |
| `setCustomer(1)` |
| `setCustomer(2)` |
| `open1()` |
| `open2()` |
| `printList(item.stockOut.id)` |
| `printProductList(item.stockOut.id)` |
| `deleteStock(item.stockOut.id)` |
| `getSupplierListFactory.nextPage()` |
| `setParam()` |
| `importModal=false` |

**跳转到**：`addDelivery`

**下拉数据源（ng-options）**

```
x.id as x.name for x in outType
x.id as x.name for x in storehouseArr
```

### 3.41 `goods.materialCompanyDelivery`

- **URL**：`/materialCompanyDelivery`
- **模板**：`views/materialAdmin/materialDelivery.html`
- **控制器**：`materialDeliveryCtrl`
- **端点数**：14

**调用的端点**

| 动作 | 端点 |
|---|---|
| `deleteStockIn` | `POST /admin/deleteStockIn.json` |
| `deleteStockOut` | `POST /admin/deleteStockOut.json` |
| `deleteStockTaking` | `POST /admin/deleteStockTaking.json` |
| `getCorpInfo` | `POST /admin/getCorpInfo.json` |
| `getStockInVoList` | `POST /admin/getStockInVoList.json` |
| `getStockOutProductVoList` | `POST /admin/getStockOutProductVoList.json` |
| `getStockOutVo` | `POST /admin/getStockOutVo.json` |
| `getStockOutVoList` | `POST /admin/getStockOutVoList.json` |
| `getStockTakingProductVoList` | `POST /admin/getStockTakingProductVoList.json` |
| `getStockTakingVo` | `POST /admin/getStockTakingVo.json` |
| `getStockTakingVoList` | `POST /admin/getStockTakingVoList.json` |
| `getStorehouseVo` | `POST /admin/getStorehouseVo.json` |
| `isAdminRoleStateOK` | `POST /admin/isAdminRoleStateOK.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 出库单号 |
| 2 | 出库日期 |
| 3 | 所属仓库 |
| 4 | 出库方式 |
| 5 | 领用人员 |
| 6 | 制单人 |
| 7 | 状态 |
| 8 | 操作 |
| 9 | 序号 |
| 10 | 名称 |
| 11 | 规格 |
| 12 | 零售价/单位 |
| 13 | 出库数量 |
| 14 | 生产厂商 |
| 15 | 成本价 |
| 16 | 成本合计 |
| 17 | 批号 |
| 18 | 有效期 |
| 19 | 序号 |
| 20 | 名称 |
| 21 | 规格 |
| 22 | 零售价/单位 |
| 23 | 出库数量 |
| 24 | 成本合计 |
| 25 | 生产厂商 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.storehouseId` |
| `obj.outType` |
| `obj.startTime` |
| `rightTime` |
| `obj.id` |
| `obj.keyword` |
| `obj.modelKeyword` |
| `param.storehouseId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `tab` |
| `item.stockOut.id` |
| `item.stockOut.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.storehouse.name` |
| `item.stockOut.outType` |
| `outType` |
| `item.drawEmployee.employeeName` |
| `item.stockOut.createName` |
| `item.stockOut.checked` |
| `supplierChecked` |
| `companyFactory.object.logo` |
| `companyFactory.object.corporationName` |
| `getCashflowObjectFactory.object.stockOut.id` |
| `getCashflowObjectFactory.object.stockOut.gmtCreate` |
| `getCashflowObjectFactory.object.stockOut.createName` |
| `getCashflowObjectFactory.object.stockOut.outDate` |
| `getCashflowObjectFactory.object.stockOut.outType` |
| `getCashflowObjectFactory.object.drawEmployee.employeeName` |
| `getCashflowObjectFactory.object.storehouse.name` |
| `getCashflowObjectFactory.object.stockOut.checkDate` |
| `getCashflowObjectFactory.object.stockOut.checkName` |
| `getCashflowObjectFactory.object.stockOut.remark` |
| `index` |
| `item.product.productName` |
| `item.productSku.model1` |
| `printModel` |
| `item.productSku.model2` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.stockOutSku.outCount` |
| `item.product.factory` |
| `item.stockInSku.skuPrice` |
| `toFixed` |
| `item.stockOutSku.outTotalCostPrice` |
| `item.stockOutSku.batchNo` |
| `item.stockOutSku.expiresDate` |
| `getStockOutObjectFactory.object.stockOut.id` |
| `getStockOutObjectFactory.object.stockOut.gmtCreate` |
| `getStockOutObjectFactory.object.stockOut.createName` |
| `getStockOutObjectFactory.object.stockOut.outDate` |
| `getStockOutObjectFactory.object.stockOut.outType` |
| `getStockOutObjectFactory.object.drawEmployee.employeeName` |
| `getStockOutObjectFactory.object.storehouse.name` |
| `getStockOutObjectFactory.object.stockOut.checkDate` |
| `getStockOutObjectFactory.object.stockOut.checkName` |
| `getStockOutObjectFactory.object.stockOut.remark` |
| `item.stockOutProduct.outCount` |
| `item.stockOutProduct.outTotalCostPrice` |
| `item.storehouse.id` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setProduct(1)` |
| `setProduct(2)` |
| `importModal=true` |
| `selectedStore()` |
| `setCustomer(null)` |
| `setCustomer(1)` |
| `setCustomer(2)` |
| `open1()` |
| `open2()` |
| `printList(item.stockOut.id)` |
| `printProductList(item.stockOut.id)` |
| `deleteStock(item.stockOut.id)` |
| `getSupplierListFactory.nextPage()` |
| `setParam()` |
| `importModal=false` |

**跳转到**：`addDelivery`

**下拉数据源（ng-options）**

```
x.id as x.name for x in outType
x.id as x.name for x in storehouseArr
```

### 3.42 `materialImportRecord`

- **URL**：`/materialImportRecord`
- **模板**：`views/materialAdmin/materialImportRecord.html`
- **控制器**：`materialImportRecordCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 入库单号 |
| 2 | 入库日期 |
| 3 | 所属仓库 |
| 4 | 入库类型 |
| 5 | 供应商 |
| 6 | 制单人 |
| 7 | 状态 |
| 8 | 操作 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockListFactory.count` |
| `getStoreNameFactory.result.object.storehouse.name` |
| `item.stockIn.id` |
| `item.stockIn.inDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.storehouse.name` |
| `item.stockIn.inType` |
| `inType` |
| `item.supplier.supplierName` |
| `item.stockIn.createName` |
| `item.stockIn.checked` |
| `supplierChecked` |

**页面动作（ng-click）**

| 动作 |
|---|
| `deleteStock(item.stockIn.id)` |

**跳转到**：`addMultiReceipts`, `goods.companyMaterialReceipts`, `materialReceipts`

### 3.43 `goods.companyImportRecord`

- **URL**：`/companyImportRecord?storehouseId`
- **模板**：`views/materialAdmin/materialImportRecord.html`
- **控制器**：`materialImportRecordCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 入库单号 |
| 2 | 入库日期 |
| 3 | 所属仓库 |
| 4 | 入库类型 |
| 5 | 供应商 |
| 6 | 制单人 |
| 7 | 状态 |
| 8 | 操作 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockListFactory.count` |
| `getStoreNameFactory.result.object.storehouse.name` |
| `item.stockIn.id` |
| `item.stockIn.inDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.storehouse.name` |
| `item.stockIn.inType` |
| `inType` |
| `item.supplier.supplierName` |
| `item.stockIn.createName` |
| `item.stockIn.checked` |
| `supplierChecked` |

**页面动作（ng-click）**

| 动作 |
|---|
| `deleteStock(item.stockIn.id)` |

**跳转到**：`addMultiReceipts`, `goods.companyMaterialReceipts`, `materialReceipts`

### 3.44 `materialInventory`

- **URL**：`/materialInventory`
- **模板**：`views/materialAdmin/materialInventory.html`
- **控制器**：`materialInventoryCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 盘点单号 |
| 2 | 盘点日期 |
| 3 | 所属仓库 |
| 4 | 制单人 |
| 5 | 状态 |
| 6 | 操作 |
| 7 | 序号 |
| 8 | 名称 |
| 9 | 规格 |
| 10 | 零售价/单位 |
| 11 | 供应商 |
| 12 | 批号 |
| 13 | 账面数量 |
| 14 | 实际数量 |
| 15 | 盘盈盘亏 |
| 16 | 序号 |
| 17 | 名称 |
| 18 | 规格 |
| 19 | 零售价/单位 |
| 20 | 账面数量 |
| 21 | 实际数量 |
| 22 | 盘盈盘亏 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.storehouseId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `tab` |
| `item.stockTaking.id` |
| `item.stockTaking.takingDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.storehouse.name` |
| `item.stockTaking.createName` |
| `item.stockTaking.checked` |
| `supplierChecked` |
| `companyFactory.object.logo` |
| `companyFactory.object.corporationName` |
| `getCashflowObjectFactory.object.stockTaking.id` |
| `getCashflowObjectFactory.object.storehouse.name` |
| `getCashflowObjectFactory.object.stockTaking.createName` |
| `getCashflowObjectFactory.object.stockTaking.checkName` |
| `index` |
| `item.product.productName` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockInSku.remark` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.supplier.supplierName` |
| `item.stockInSku.batchNo` |
| `item.stockTakingSku.oldCount` |
| `item.stockTakingSku.newCount` |
| `getProductObjectFactory.object.stockTaking.id` |
| `getProductObjectFactory.object.storehouse.name` |
| `getProductObjectFactory.object.stockTaking.createName` |
| `getProductObjectFactory.object.stockTaking.checkName` |
| `item.stockTakingProduct.oldCount` |
| `item.stockTakingProduct.newCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setShowMoreFun(false,$event)` |
| `setCustomer(1)` |
| `setCustomer(2)` |
| `setShowMoreFun(true,$event)` |
| `jump($event)` |
| `openBivariate()` |
| `printListProduct(item.stockTaking.id)` |
| `printList(item.stockTaking.id)` |
| `deleteStock(item.stockTaking.id)` |

**跳转到**：`addInventory`

**下拉数据源（ng-options）**

```
x.id as x.name for x in storehouseArr
```

### 3.45 `goods.materialCompanyInventory`

- **URL**：`/materialCompanyInventory`
- **模板**：`views/materialAdmin/materialInventory.html`
- **控制器**：`materialInventoryCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 盘点单号 |
| 2 | 盘点日期 |
| 3 | 所属仓库 |
| 4 | 制单人 |
| 5 | 状态 |
| 6 | 操作 |
| 7 | 序号 |
| 8 | 名称 |
| 9 | 规格 |
| 10 | 零售价/单位 |
| 11 | 供应商 |
| 12 | 批号 |
| 13 | 账面数量 |
| 14 | 实际数量 |
| 15 | 盘盈盘亏 |
| 16 | 序号 |
| 17 | 名称 |
| 18 | 规格 |
| 19 | 零售价/单位 |
| 20 | 账面数量 |
| 21 | 实际数量 |
| 22 | 盘盈盘亏 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.storehouseId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `tab` |
| `item.stockTaking.id` |
| `item.stockTaking.takingDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.storehouse.name` |
| `item.stockTaking.createName` |
| `item.stockTaking.checked` |
| `supplierChecked` |
| `companyFactory.object.logo` |
| `companyFactory.object.corporationName` |
| `getCashflowObjectFactory.object.stockTaking.id` |
| `getCashflowObjectFactory.object.storehouse.name` |
| `getCashflowObjectFactory.object.stockTaking.createName` |
| `getCashflowObjectFactory.object.stockTaking.checkName` |
| `index` |
| `item.product.productName` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockInSku.remark` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.supplier.supplierName` |
| `item.stockInSku.batchNo` |
| `item.stockTakingSku.oldCount` |
| `item.stockTakingSku.newCount` |
| `getProductObjectFactory.object.stockTaking.id` |
| `getProductObjectFactory.object.storehouse.name` |
| `getProductObjectFactory.object.stockTaking.createName` |
| `getProductObjectFactory.object.stockTaking.checkName` |
| `item.stockTakingProduct.oldCount` |
| `item.stockTakingProduct.newCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setShowMoreFun(false,$event)` |
| `setCustomer(1)` |
| `setCustomer(2)` |
| `setShowMoreFun(true,$event)` |
| `jump($event)` |
| `openBivariate()` |
| `printListProduct(item.stockTaking.id)` |
| `printList(item.stockTaking.id)` |
| `deleteStock(item.stockTaking.id)` |

**跳转到**：`addInventory`

**下拉数据源（ng-options）**

```
x.id as x.name for x in storehouseArr
```

### 3.46 `materialOutportRecord`

- **URL**：`/materialOutportRecord?storehouseId`
- **模板**：`views/materialAdmin/materialOutportRecord.html`
- **控制器**：`materialOutportRecordCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 出库单号 |
| 2 | 出库日期 |
| 3 | 所属仓库 |
| 4 | 出库类型 |
| 5 | 领用人员 |
| 6 | 制单人 |
| 7 | 状态 |
| 8 | 操作 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockListFactory.count` |
| `getStoreNameFactory.result.object.storehouse.name` |
| `item.stockOut.id` |
| `item.stockOut.outDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.storehouse.name` |
| `item.stockOut.outType` |
| `outType` |
| `item.drawEmployee.employeeName` |
| `item.stockOut.createName` |
| `item.stockOut.checked` |
| `supplierChecked` |

**页面动作（ng-click）**

| 动作 |
|---|
| `deleteStock(item.stockOut.id)` |

**跳转到**：`goods.materialCompanyDelivery`, `materialDelivery`

### 3.47 `goods.materialCompanyOutportRecord`

- **URL**：`/materialCompanyOutportRecord?storehouseId`
- **模板**：`views/materialAdmin/materialOutportRecord.html`
- **控制器**：`materialOutportRecordCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 出库单号 |
| 2 | 出库日期 |
| 3 | 所属仓库 |
| 4 | 出库类型 |
| 5 | 领用人员 |
| 6 | 制单人 |
| 7 | 状态 |
| 8 | 操作 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockListFactory.count` |
| `getStoreNameFactory.result.object.storehouse.name` |
| `item.stockOut.id` |
| `item.stockOut.outDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.storehouse.name` |
| `item.stockOut.outType` |
| `outType` |
| `item.drawEmployee.employeeName` |
| `item.stockOut.createName` |
| `item.stockOut.checked` |
| `supplierChecked` |

**页面动作（ng-click）**

| 动作 |
|---|
| `deleteStock(item.stockOut.id)` |

**跳转到**：`goods.materialCompanyDelivery`, `materialDelivery`

### 3.48 `purchase.materialPurchase`

- **URL**：`/materialPurchase`
- **模板**：`views/materialAdmin/materialPurchase.html`
- **控制器**：`materialPurchaseCtrl`
- **端点数**：14

**调用的端点**

| 动作 | 端点 |
|---|---|
| `cancelStockPurchase` | `POST /admin/cancelStockPurchase.json` |
| `commitStockPurchaseList` | `POST /admin/commitStockPurchaseList.json` |
| `commitStockPurchaseOut` | `POST /admin/commitStockPurchaseOut.json` |
| `deleteStockPurchase` | `POST /admin/deleteStockPurchase.json` |
| `getChildrenLinkAndCode` | `POST /admin/getChildrenLinkAndCode.json` |
| `getCorpInfo` | `POST /admin/getCorpInfo.json` |
| `getPurchaseRequestVoList` | `POST /admin/getPurchaseRequestVoList.json` |
| `getStockPurchaseOutSkuList` | `POST /admin/getStockPurchaseOutSkuList.json` |
| `getStockPurchaseVo` | `POST /admin/getStockPurchaseVo.json` |
| `getStockPurchaseVoList` | `POST /admin/getStockPurchaseVoList.json` |
| `getStorehouseVo` | `POST /admin/getStorehouseVo.json` |
| `getSupplier` | `POST /admin/getSupplier.json` |
| `reCreateStockPurchaseAndSkuList` | `POST /admin/reCreateStockPurchaseAndSkuList.json` |
| `updateStockPurchaseOutSkuList` | `POST /admin/updateStockPurchaseOutSkuList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 采购单号 |
| 2 | 供应商 |
| 3 | 制单人 |
| 4 | 采购员 |
| 5 | 采购日期 |
| 6 | 采购类型 |
| 7 | 产品名称 |
| 8 | 状态 |
| 9 | 操作 |
| 10 | 序号 |
| 11 | 名称 |
| 12 | 规格 |
| 13 | 采购价/单位 |
| 14 | 订货信息 |
| 15 | 采购数量 |
| 16 | 小计 |
| 17 | 备注 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `rightTime` |
| `obj.id` |
| `obj.customerKeyword` |
| `obj.keyword` |
| `obj.modelKeyword` |
| `obj.orderModelKeyword` |
| `multipleChoose.isAll` |
| `multipleChoose.multiChooseList[$index+getStockListFactory.index-pageSize]` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getPurchaseRequestCountListFactory.count` |
| `item.stockPurchase.id` |
| `item.medicalProduct.productName` |
| `item.supplier.supplierName` |
| `item.stockPurchase.createName` |
| `item.stockPurchase.purchaser` |
| `item.stockPurchase.purchaseDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.stockPurchase.productType` |
| `purchaseType` |
| `item.productNames` |
| `item.stockPurchase.checked` |
| `supplierChecked` |
| `item.stockPurchase.allIn` |
| `allIn` |
| `companyFactory.object.logo` |
| `companyFactory.object.corporationName` |
| `getCashflowObjectFactory.result.object.stockPurchase.id` |
| `getCashflowObjectFactory.result.object.supplier.supplierName` |
| `getCashflowObjectFactory.result.object.stockPurchase.purchaser` |
| `getCashflowObjectFactory.result.object.stockPurchase.createName` |
| `getCashflowObjectFactory.result.object.stockPurchase.remark` |
| `index` |
| `item.product.productName` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockPurchaseSku.skuPrice` |
| `item.productSku.unitName` |
| `item.stockPurchaseSku.customerInfo.customerName` |
| `item.requestSkuMergeRemark` |
| `item.stockPurchaseSku.skuCount` |
| `item.stockPurchaseSku.skuTotalPrice` |
| `item.stockPurchaseSku.remark` |
| `totalCount` |
| `getCashflowObjectFactory.object.stockPurchase.totalPrice` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `setType(null)` |
| `setType(1)` |
| `setType(2)` |
| `setTab(null)` |
| `setTab(0)` |
| `setTab(1)` |
| `setTab(2)` |
| `setTab(3)` |
| `setTab(4)` |
| `multipleChoose.batchAudit()` |
| `multipleChoose.checkAll()` |
| `multipleChoose.choseSingle()` |
| `printList(item.stockPurchase.id)` |
| `anotherRequest(item.stockPurchase.id)` |
| `cancelStockPurchase(item)` |
| `deleteStock(item.stockPurchase.id)` |

**跳转到**：`purchase.addPurchasement`, `purchase.addSalePurchase`, `purchase.materialPurchaseReturn`, `purchase.purchaseRequestCheck`

### 3.49 `purchase.materialPurchaseBackGoods`

- **URL**：`/materialPurchaseBackGoods?stockPurchaseOutId&storehouseId`
- **模板**：`views/materialAdmin/materialPurchaseBackGoods.html`
- **控制器**：`materialPurchaseBackGoodsCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| {{'采购退货'}} |
| {{supplierName}} |
| {{newDate \| date:"yyyy-MM-dd"}} |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 入库单价 |
| 7 | 退货数量 |
| 8 | 退货单价 |
| 9 | 退货总价 |
| 10 | 生产日期 |
| 11 | 批号 |
| 12 | 有效期 |
| 13 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `create.stockOutDate` |
| `item.outCount` |
| `item.outSkuPrice` |
| `create.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `supplierName` |
| `newDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `item.model1Name` |
| `item.model1` |
| `item.model2Name` |
| `item.model2` |
| `item.unLockExistSkuCount` |
| `item.skuPrice` |
| `item.outSkuPrice` |
| `item.outCount` |
| `item.productionDateLong` |
| `item.batchNo` |
| `item.expiresDateLong` |
| `toutle.num` |
| `toutle.money` |
| `storeName` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `getChuKuCangKu()` |
| `deleteReceipt($index)` |
| `sureBackGoods()` |
| `saveDelivery()` |
| `hideProductModal()` |

**跳转到**：`purchase.materialPurchaseReturn`

### 3.50 `purchase.materialPurchaseBackLook`

- **URL**：`/materialPurchaseBackLook?stockPurchaseOutId&storehouseId`
- **模板**：`views/materialAdmin/materialPurchaseBackLook.html`
- **控制器**：`materialPurchaseBackLookCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `createStockPurchaseOutAndSkuList` | `POST /admin/createStockPurchaseOutAndSkuList.json` |
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getProductSkuInVoList` | `POST /admin/getProductSkuInVoList.json` |
| `getStockPurchaseOutSkuList` | `POST /admin/getStockPurchaseOutSkuList.json` |
| `getStorehouseVo` | `POST /admin/getStorehouseVo.json` |

**表单标签**

| 标签 |
|---|
| {{stockOutDate \| date:"yyyy-MM-dd"}} |
| {{'采购出库'}} |
| {{supplierName}} |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 入库单价 |
| 7 | 退货数量 |
| 8 | 退货单价 |
| 9 | 退货总价 |
| 10 | 生产日期 |
| 11 | 批号 |
| 12 | 有效期 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `item.outCount` |
| `item.outSkuPrice` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `stockOutDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `supplierName` |
| `getStockTakingObjectFactory.object.allIn` |
| `allIn` |
| `msgObj.stockPurchaseOut.id` |
| `msgObj.stockPurchaseOut.gmtCreate` |
| `msgObj.stockPurchaseOut.createName` |
| `msgObj.stockPurchaseOut.stockOutDate` |
| `msgObj.stockPurchaseOut.checkName` |
| `msgObj.stockPurchaseOut.purchaser` |
| `msgObj.stockPurchaseOut.checkDate` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `item.model1Name` |
| `item.model1` |
| `item.model2Name` |
| `item.model2` |
| `item.unLockExistSkuCount` |
| `item.skuPrice` |
| `item.outCount` |
| `item.outSkuPrice` |
| `item.productionDateLong` |
| `item.batchNo` |
| `item.expiresDateLong` |
| `toutle.num` |
| `toutle.money` |
| `storeName` |
| `create.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `getChuKuCangKu()` |
| `hideProductModal()` |

**跳转到**：`purchase.materialPurchaseReturn`

### 3.51 `purchase.materialPurchaseBackOne`

- **URL**：`/materialPurchaseBackOne?id&type&stockPurchaseOutId`
- **模板**：`views/materialAdmin/materialPurchaseBackOne.html`
- **控制器**：`materialPurchaseBackOneCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 入库单价 |
| 7 | 退货数量 |
| 8 | 退货单价 |
| 9 | 退货总价 |
| 10 | 生产日期 |
| 11 | 批号 |
| 12 | 有效期 |
| 13 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `create.stockOutDate` |
| `item.outCount` |
| `item.outSkuPrice` |
| `obj.remark` |
| `create.remark` |
| `obj.keyword` |
| `obj.modelKeyword` |
| `product.productSku` |
| `obj.brandId` |
| `select.stockInSkuId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `item.model1Name` |
| `item.model1` |
| `item.model2Name` |
| `item.model2` |
| `item.unLockExistSkuCount` |
| `item.skuPrice` |
| `item.outSkuPrice` |
| `item.outCount` |
| `item.productionDateLong` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.batchNo` |
| `item.expiresDateLong` |
| `toutle.num` |
| `toutle.money` |
| `storeName` |
| `item.product.productName` |
| `item.productSku.model2` |
| `item.productSku.model1` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `province.id` |
| `province.brandName` |
| `getProductListFactory.items` |
| `select.idx` |
| `unLockExistSkuCount` |
| `iten.unLockExistSkuCount` |
| `iten.stockIn.inDate` |
| `iten.storehouse.name` |
| `iten.stockInSku.productionDate` |
| `iten.stockInSku.expiresDate` |
| `iten.stockInSku.batchNo` |
| `ite.modelName` |
| `ite.modelValue` |
| `product.model1Name` |
| `product.model2Name` |
| `iten.stockInSku.remark` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `getChuKuCangKu()` |
| `deleteReceipt($index)` |
| `showAddModal()` |
| `addDelivery()` |
| `selectProductName(item.productSku.id,$index)` |
| `getProductListFactory.nextPage()` |
| `getPiCiMsg()` |
| `setstockInSkuId(iten.stockInSku.id,$index)` |
| `selectProduct()` |
| `hideProductModal()` |

**跳转到**：`purchase.materialPurchaseReturn`

### 3.52 `materialPurchaseRequest`

- **URL**：`/materialPurchaseRequest`
- **模板**：`views/materialAdmin/materialPurchaseRequest.html`
- **控制器**：`materialPurchaseRequestCtrl`
- **端点数**：11

**调用的端点**

| 动作 | 端点 |
|---|---|
| `commitPurchaseRequestList` | `POST /admin/commitPurchaseRequestList.json` |
| `delStockPurchaseOutByIdBeforeCheckd` | `POST /admin/delStockPurchaseOutByIdBeforeCheckd.json` |
| `deletePurchaseRequest` | `POST /admin/deletePurchaseRequest.json` |
| `getCorpInfo` | `POST /admin/getCorpInfo.json` |
| `getPurchaseRequestVoList` | `POST /admin/getPurchaseRequestVoList.json` |
| `getPurchaseRequestVoListOfCompany` | `POST /admin/getPurchaseRequestVoListOfCompany.json` |
| `getStockPurchaseOutList` | `POST /admin/getStockPurchaseOutList.json` |
| `getStockPurchaseOutSkuList` | `POST /admin/getStockPurchaseOutSkuList.json` |
| `getStorehouseListOfMine` | `POST /admin/getStorehouseListOfMine.json` |
| `getSupplier` | `POST /admin/getSupplier.json` |
| `reSendPurchaseRequest` | `POST /admin/reSendPurchaseRequest.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 采购申请号 |
| 2 | {{corpInfo. companyTitle}} |
| 3 | 申请人 |
| 4 | 时间要求 |
| 5 | 采购类型 |
| 6 | 产品名称 |
| 7 | 申请状态 |
| 8 | 采购订单 采购申请提交后，由采购员在【采购】功能中，处理采购申请。 |
| 9 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `rightTime` |
| `obj.customerKeyword` |
| `obj.keyword` |
| `multipleChoose.isAll` |
| `multipleChoose.multiChooseList[$index+getStockListFactory.index-pageSize]` |
| `obj.purchaseRequestId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `corpInfo.` |
| `companyTitle` |
| `item.purchaseRequest.id` |
| `item.medicalProduct.productName` |
| `item.company.companyName` |
| `item.purchaseRequest.createName` |
| `item.purchaseRequest.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.purchaseRequest.productType` |
| `purchaseType` |
| `item.productNames` |
| `item.purchaseRequest.checked` |
| `supplierChecked` |
| `item.purchaseRequest.processStatus` |
| `processStatus` |

**页面动作（ng-click）**

| 动作 |
|---|
| `open1()` |
| `open2()` |
| `setType(null)` |
| `setType(1)` |
| `setType(2)` |
| `setTab(null)` |
| `setTab(0)` |
| `setTab(1)` |
| `multipleChoose.batchAudit()` |
| `multipleChoose.checkAll()` |
| `multipleChoose.choseSingle()` |
| `anotherRequest(item.purchaseRequest.id)` |
| `deleteStock(item.purchaseRequest.id)` |

**跳转到**：`addPurchaseRequest`

### 3.53 `purchase.materialPurchaseReturn`

- **URL**：`/materialPurchaseReturn`
- **模板**：`views/materialAdmin/materialPurchaseReturn.html`
- **控制器**：`materialPurchaseReturnCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 供应商 |
| 3 | 退货仓库 |
| 4 | 出库方式 |
| 5 | 制单人 |
| 6 | 制单时间 |
| 7 | 状态 |
| 8 | 操作 |
| 9 | 序号 |
| 10 | 品牌/类目 |
| 11 | 商品信息 |
| 12 | 规格 |
| 13 | 可用数量 |
| 14 | 入库单价 |
| 15 | 退货数量 |
| 16 | 退货单价 |
| 17 | 总价 |
| 18 | 批号 |
| 19 | 有效期 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `rightTime` |
| `item.outCount` |
| `item.outSkuPrice` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getPurchaseRequestCountListFactory.count` |
| `item.name` |
| `index` |
| `item.supplier.supplierName` |
| `item.storehouse.name` |
| `item.stockPurchaseOut.createName` |
| `item.stockPurchaseOut.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.stockPurchaseOut.checked` |
| `item.stockPurchaseOut.allOut` |
| `companyFactory.object.logo` |
| `companyFactory.object.corporationName` |
| `printListObj.stockPurchaseOut.id` |
| `printListObj.supplier.supplierName` |
| `printListObj.stockPurchaseOut.stockOutDate` |
| `printListObj.stockPurchaseOut.createName` |
| `printListObj.stockPurchaseOut.gmtCreate` |
| `printListObj.stockPurchaseOut.checkName` |
| `printListObj.stockPurchaseOut.checkDate` |
| `printListObj.stockPurchaseOut.remark` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.skuCode` |
| `item.model1Name` |
| `item.model1` |
| `item.model2Name` |
| `item.model2` |
| `item.unLockExistSkuCount` |
| `item.skuPrice` |
| `item.outCount` |
| `item.outSkuPrice` |
| `item.batchNo` |
| `item.expiresDateLong` |
| `toutle.num` |
| `toutle.money` |

**页面动作（ng-click）**

| 动作 |
|---|
| `chooseCangKu(item)` |
| `chooseCangKu(` |
| `setType(null)` |
| `setType(1)` |
| `setType(2)` |
| `open1()` |
| `open2()` |
| `printList(item)` |
| `openDeleteDialog(item.stockPurchaseOut.id)` |

**跳转到**：`purchase.materialPurchase`, `purchase.materialPurchaseReturn`, `purchase.purchaseRequestCheck`

### 3.54 `goods.companyMaterialReceipts`

- **URL**：`/companyMaterialReceipts`
- **模板**：`views/materialAdmin/materialReceipts.html`
- **控制器**：`materialReceiptsCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `deleteStockIn` | `POST /admin/deleteStockIn.json` |
| `getStockInVoList` | `POST /admin/getStockInVoList.json` |
| `isAdminRoleStateOK` | `POST /admin/isAdminRoleStateOK.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 入库单号 |
| 2 | 入库日期 |
| 3 | 所属仓库 |
| 4 | 入库类型 |
| 5 | 供应商 |
| 6 | 制单人 |
| 7 | 状态 |
| 8 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.storehouseId` |
| `obj.inType` |
| `obj.startTime` |
| `rightTime` |
| `obj.id` |
| `obj.keyword` |
| `obj.modelKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `tab` |
| `item.stockIn.id` |
| `item.stockIn.inDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.storehouse.name` |
| `item.stockIn.inType` |
| `inType` |
| `item.supplier.supplierName` |
| `item.stockIn.createName` |
| `item.stockIn.checked` |
| `supplierChecked` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setCustomer(null)` |
| `setCustomer(1)` |
| `setCustomer(2)` |
| `open1()` |
| `open2()` |
| `printList(item.stockIn.id)` |
| `deleteStock(item.stockIn.id)` |

**跳转到**：`addMultiReceipts`, `addReceipt`

**下拉数据源（ng-options）**

```
x.id as x.name for x in inType
x.id as x.name for x in storehouseArr
```

### 3.55 `materialReceipts`

- **URL**：`/materialReceipts`
- **模板**：`views/materialAdmin/materialReceipts.html`
- **控制器**：`materialReceiptsCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `deleteStockIn` | `POST /admin/deleteStockIn.json` |
| `getStockInVoList` | `POST /admin/getStockInVoList.json` |
| `isAdminRoleStateOK` | `POST /admin/isAdminRoleStateOK.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 入库单号 |
| 2 | 入库日期 |
| 3 | 所属仓库 |
| 4 | 入库类型 |
| 5 | 供应商 |
| 6 | 制单人 |
| 7 | 状态 |
| 8 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.storehouseId` |
| `obj.inType` |
| `obj.startTime` |
| `rightTime` |
| `obj.id` |
| `obj.keyword` |
| `obj.modelKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `tab` |
| `item.stockIn.id` |
| `item.stockIn.inDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.storehouse.name` |
| `item.stockIn.inType` |
| `inType` |
| `item.supplier.supplierName` |
| `item.stockIn.createName` |
| `item.stockIn.checked` |
| `supplierChecked` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setCustomer(null)` |
| `setCustomer(1)` |
| `setCustomer(2)` |
| `open1()` |
| `open2()` |
| `printList(item.stockIn.id)` |
| `deleteStock(item.stockIn.id)` |

**跳转到**：`addMultiReceipts`, `addReceipt`

**下拉数据源（ng-options）**

```
x.id as x.name for x in inType
x.id as x.name for x in storehouseArr
```

### 3.56 `goods.modifyStockCompanyChange`

- **URL**：`/modifyStockCompanyChange?id&storehouseId`
- **模板**：`views/materialAdmin/modifyStockChange.html`
- **控制器**：`modifyStockChangeCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `checkStockTransfer` | `POST /admin/checkStockTransfer.json` |
| `getStockTransferVo` | `POST /admin/getStockTransferVo.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |
| `updateStockTransferAndSkuList` | `POST /admin/updateStockTransferAndSkuList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 出库数量 |
| 7 | 生产日期 |
| 8 | 批号 |
| 9 | 有效期 |
| 10 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.outDate` |
| `item.outCount` |
| `obj.operator` |
| `obj.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getTransferFactory.result.object.stockTransfer.id` |
| `getTransferFactory.result.object.stockTransfer.createName` |
| `getTransferFactory.result.object.outStorehouse.name` |
| `getTransferFactory.result.object.inStorehouse.name` |
| `obj.outDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `item.model1Name` |
| `item.model1` |
| `item.model2Name` |
| `item.model2` |
| `item.unLockExistSkuCount` |
| `item.productionDate` |
| `item.batchNo` |
| `item.expiresDate` |
| `totalExistCount` |
| `totalprice` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `open1()` |
| `deleteReceipt($index)` |
| `addDelivery()` |
| `checkSupplier()` |

**跳转到**：`goods.stockCompanyChange`, `stockChange`

### 3.57 `modifyStockChange`

- **URL**：`/modifyStockChange?id`
- **模板**：`views/materialAdmin/modifyStockChange.html`
- **控制器**：`modifyStockChangeCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `checkStockTransfer` | `POST /admin/checkStockTransfer.json` |
| `getStockTransferVo` | `POST /admin/getStockTransferVo.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |
| `updateStockTransferAndSkuList` | `POST /admin/updateStockTransferAndSkuList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 出库数量 |
| 7 | 生产日期 |
| 8 | 批号 |
| 9 | 有效期 |
| 10 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.outDate` |
| `item.outCount` |
| `obj.operator` |
| `obj.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getTransferFactory.result.object.stockTransfer.id` |
| `getTransferFactory.result.object.stockTransfer.createName` |
| `getTransferFactory.result.object.outStorehouse.name` |
| `getTransferFactory.result.object.inStorehouse.name` |
| `obj.outDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `item.model1Name` |
| `item.model1` |
| `item.model2Name` |
| `item.model2` |
| `item.unLockExistSkuCount` |
| `item.productionDate` |
| `item.batchNo` |
| `item.expiresDate` |
| `totalExistCount` |
| `totalprice` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `open1()` |
| `deleteReceipt($index)` |
| `addDelivery()` |
| `checkSupplier()` |

**跳转到**：`goods.stockCompanyChange`, `stockChange`

### 3.58 `goods.modifyStockProductChange`

- **URL**：`/modifyStockProductChange?id&storehouseId`
- **模板**：`views/materialAdmin/modifyStockProductChange.html`
- **控制器**：`modifyStockProductChangeCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `commitStockTransferByProductSku` | `POST /admin/commitStockTransferByProductSku.json` |
| `getStockPurchaseVo` | `POST /admin/getStockPurchaseVo.json` |
| `getStockTransferProductVoList` | `POST /admin/getStockTransferProductVoList.json` |
| `getStockTransferVo` | `POST /admin/getStockTransferVo.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |
| `updateStockTransferByProductSku` | `POST /admin/updateStockTransferByProductSku.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 出库数量 |
| 7 | 有效期 |
| 8 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.outDate` |
| `item.stockTransferProduct.transferCount` |
| `obj.operator` |
| `obj.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getTransferFactory.result.object.stockTransfer.id` |
| `getTransferFactory.result.object.stockTransfer.createName` |
| `getTransferFactory.result.object.outStorehouse.name` |
| `getTransferFactory.result.object.inStorehouse.name` |
| `obj.outDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.factory` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.unLockExistSkuCount` |
| `totalExistCount` |
| `totalprice` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `open1()` |
| `deleteReceipt($index)` |
| `addDelivery()` |
| `checkSupplier()` |

**跳转到**：`goods.stockCompanyChange`, `stockChange`

### 3.59 `purchaseDetail`

- **URL**：`/purchaseDetail?purchaseId`
- **模板**：`views/materialAdmin/purchaseDetail.html`
- **控制器**：`purchaseDetailCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品规格信息 |
| 4 | 采购数量 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockTakingObjectFactory.result.object.supplier.supplierName` |
| `getStockTakingObjectFactory.result.object.stockPurchase.purchaser` |
| `getStockTakingObjectFactory.result.object.stockPurchase.remark` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.stockPurchaseSku.productName` |
| `item.stockPurchaseSku.model1` |
| `item.stockPurchaseSku.model2` |
| `item.product.factory` |
| `item.stockPurchaseSku.skuPrice` |
| `item.stockPurchaseSku.unitName` |
| `item.product.productCode` |
| `item.stockPurchaseSku.skuCode` |
| `item.stockPurchaseSku.skuCount` |

**跳转到**：`materialInventory`

### 3.60 `purchase.purchaseModify`

- **URL**：`/purchaseModify?purchaseId`
- **模板**：`views/materialAdmin/purchaseModify.html`
- **控制器**：`purchaseModifyCtrl`
- **端点数**：25

**调用的端点**

| 动作 | 端点 |
|---|---|
| `checkDeletePurchaseRequestSku` | `POST /admin/checkDeletePurchaseRequestSku.json` |
| `checkDeleteStockPurchaseSku` | `POST /admin/checkDeleteStockPurchaseSku.json` |
| `commitPurchaseRequest` | `POST /admin/commitPurchaseRequest.json` |
| `commitStockPurchase` | `POST /admin/commitStockPurchase.json` |
| `commitStockPurchaseIn` | `POST /admin/commitStockPurchaseIn.json` |
| `computePrice` | `POST /admin/computePrice.json` |
| `createStockPurchaseFromRequest` | `POST /admin/createStockPurchaseFromRequest.json` |
| `createStockPurchaseInAndSkuList` | `POST /admin/createStockPurchaseInAndSkuList.json` |
| `deletePurchaseRequest` | `POST /admin/deletePurchaseRequest.json` |
| `getChildrenLinkAndCode` | `POST /admin/getChildrenLinkAndCode.json` |
| `getCompanyList` | `POST /admin/getCompanyList.json` |
| `getCorpInfo` | `POST /admin/getCorpInfo.json` |
| `getPurchaseRequestVo` | `POST /admin/getPurchaseRequestVo.json` |
| `getPurchaseRequestVoList` | `POST /admin/getPurchaseRequestVoList.json` |
| `getStockPurchaseVo` | `POST /admin/getStockPurchaseVo.json` |
| `getStockPurchaseVoWithExistSkuCount` | `POST /admin/getStockPurchaseVoWithExistSkuCount.json` |
| `getStorehouseVo` | `POST /admin/getStorehouseVo.json` |
| `getSupplierList` | `POST /admin/getSupplierList.json` |
| `isPurchaseRequestProcessed` | `POST /admin/isPurchaseRequestProcessed.json` |
| `mergePurchaseRequestSku` | `POST /admin/mergePurchaseRequestSku.json` |
| `selectModelValueList` | `POST /admin/selectModelValueList.json` |
| `selectStockPurchaseInVoList` | `POST /admin/selectStockPurchaseInVoList.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |
| `updatePurchaseRequestAndSkuList` | `POST /admin/updatePurchaseRequestAndSkuList.json` |
| `updateStockPurchaseAndSkuList` | `POST /admin/updateStockPurchaseAndSkuList.json` |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `purchase.purchaseDate` |
| `purchase.purchaser` |
| `purchase.remark` |
| `item.stockPurchaseSku.skuCount` |
| `item.stockPurchaseSku.skuPrice` |
| `item.stockPurchaseSku.skuTotalPrice` |
| `iten.modelValue` |
| `item.stockPurchaseSku.remark` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.stockPurchaseSku.productName` |
| `item.product.factory` |
| `item.stockPurchaseSku.skuPrice` |
| `item.stockPurchaseSku.unitName` |
| `item.product.productCode` |
| `item.stockPurchaseSku.skuCode` |
| `item.product.model1Name` |
| `item.stockPurchaseSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.stockPurchaseSku.model2` |
| `item.stockPurchaseSku.customerInfo.customerName` |
| `item.requestSkuMergeRemark` |
| `iten.modelName` |
| `item.value` |
| `totalCount` |
| `totalCountPrice` |
| `toFixed` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `open1()` |
| `showMore(item.stockPurchaseSku.id,$event)` |
| `deleteReceipt(item.stockPurchaseSku.id,$index)` |
| `getModelValue(iten.modelNameId,outerIndex,innerIndex,$event)` |
| `selectModelName(item.value)` |
| `saveInventory()` |
| `checkSupplier()` |

**跳转到**：`purchase.materialPurchase`

### 3.61 `purchase.purchaseReciept`

- **URL**：`/purchaseReciept?purchaseId`
- **模板**：`views/materialAdmin/purchaseReciept.html`
- **控制器**：`purchaseRecieptCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品基本信息 |
| 4 | 规格 |
| 5 | 生产厂家 |
| 6 | 生产许可证号 |
| 7 | 订货信息 |
| 8 | 采购数量 |
| 9 | 已入库数 |
| 10 | 本次入库数 |
| 11 | 批号 |
| 12 | 生产日期 |
| 13 | 有效期 |
| 14 | 唯一标识码 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `purchase.storehouseId` |
| `item.inSkuCount` |
| `item.batchNo` |
| `item.productionDate` |
| `item.expiresDate` |
| `purchase.stockInDate` |
| `purchase.operator` |
| `purchase.remark` |
| `tab.amount` |
| `tab.batchNo` |
| `tab.time` |
| `tab.time2` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockTakingObjectFactory.object.allIn` |
| `allIn` |
| `getStockTakingObjectFactory.object.stockPurchase.id` |
| `getStockTakingObjectFactory.object.supplier.supplierName` |
| `getStockTakingObjectFactory.object.stockPurchase.purchaser` |
| `getStockTakingObjectFactory.object.stockPurchase.createName` |
| `getStockTakingObjectFactory.object.stockPurchase.remark` |
| `item.rowSpan` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.factory` |
| `item.skuPrice` |
| `item.unitName` |
| `item.productCode` |
| `item.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.model1Name` |
| `item.model1` |
| `printModel` |
| `item.model2Name` |
| `item.model2` |
| `item.remark` |
| `item.factoryLicense` |
| `item.customerName` |
| `item.requestSkuMergeRemark` |
| `item.skuCount` |
| `item.existSkuCount` |
| `item.uniqueCode` |
| `item.stockPurchaseIn.id` |
| `iten.stockPurchaseInSkuList.length` |
| `iten.brand.brandName` |
| `iten.category.categoryName` |
| `iten.product.productName` |
| `iten.product.factory` |
| `iten.stockPurchaseSku.skuPrice` |
| `iten.productSku.unitName` |
| `iten.product.productCode` |
| `iten.productSku.skuCode` |
| `item.modelName` |
| `item.modelValue` |
| `iten.product.model1Name` |
| `iten.stockPurchaseSku.model1` |
| `iten.product.model2Name` |
| `iten.stockPurchaseSku.model2` |
| `iten.stockPurchaseSku.remark` |
| `iten.product.factoryLicense` |
| `iten.stockPurchaseSku.customerInfo.customerName` |
| `iten.requestSkuMergeRemark` |
| `iten.stockPurchaseSku.skuCount` |
| `iten.inSkuCount` |
| `iten.batchNo` |
| `iten.productionDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `iten.expiresDate` |
| `iten.uniqueCode` |
| `item.stockPurchaseIn.stockInId` |
| `item.stockPurchaseIn.stockInDate` |
| `item.storehouse.name` |
| `item.stockPurchaseIn.operator` |
| `item.stockPurchaseIn.remark` |
| `getStoreName.result.object.storehouse.name` |
| `goodsType` |
| `goodsCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `toggleAddReciept()` |
| `bindUdi.setShow(true)` |
| `showAddPurchase()` |
| `bindUdi.allChoseFun()` |
| `setTab(2)` |
| `setTab(4)` |
| `setTab(3)` |
| `bindUdi.choseSingle(item)` |
| `showMore(item.stockPurchaseSkuId,$event)` |
| `open1()` |
| `toggleReciept()` |
| `showMore(item.stockPurchaseSku.id,$event)` |
| `printRukudan.open(true,item)` |
| `open2()` |
| `setAllProduct()` |
| `setAllModal=false` |
| `addPurchase()` |
| `setToModal=false` |

**跳转到**：`purchase.materialPurchase`

**下拉数据源（ng-options）**

```
x.id as x.name for x in storehouseArr
```

### 3.62 `purchase.purchaseRecieptDetail`

- **URL**：`/purchaseRecieptDetail?purchaseId`
- **模板**：`views/materialAdmin/purchaseRecieptDetail.html`
- **控制器**：`purchaseRecieptCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品基本信息 |
| 4 | 规格 |
| 5 | 订货信息 |
| 6 | 采购数量 |
| 7 | 小计 |
| 8 | 已入库数 |
| 9 | 待入库数 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockTakingObjectFactory.object.allIn` |
| `allIn` |
| `getStockTakingObjectFactory.object.stockPurchase.id` |
| `getStockTakingObjectFactory.object.stockPurchase.createName` |
| `getStockTakingObjectFactory.object.supplier.supplierName` |
| `getStockTakingObjectFactory.object.stockPurchase.purchaser` |
| `getStockTakingObjectFactory.object.stockPurchase.remark` |
| `getStockTakingObjectFactory.object.stockPurchase.checkName` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.factory` |
| `item.skuPrice` |
| `item.unitName` |
| `item.productCode` |
| `item.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.model1Name` |
| `item.model1` |
| `printModel` |
| `item.model2Name` |
| `item.model2` |
| `item.remark` |
| `item.customerName` |
| `item.requestSkuMergeRemark` |
| `item.skuCount` |
| `item.skuTotalPrice` |
| `item.existSkuCount` |
| `item.inSkuCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `showMore(item.id,$event)` |

**跳转到**：`purchase.materialPurchase`

### 3.63 `purchase.purchaseRequestCheck`

- **URL**：`/purchaseRequestCheck`
- **模板**：`views/materialAdmin/purchaseRequestCheck.html`
- **控制器**：`purchaseRequestCheckCtrl`
- **端点数**：0

**表单标签**

| 标签 |
|---|
| 全部 {{item.companyName}} 全部 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 全部 |
| 2 | 采购申请号 |
| 3 | {{corpInfo. companyTitle}} |
| 4 | 申请人 |
| 5 | 时间要求 |
| 6 | 采购类型 |
| 7 | 产品名称 |
| 8 | 采购订单 |
| 9 | 操作 |
| 10 | 序号 |
| 11 | 品牌/类目 |
| 12 | 商品基本信息 |
| 13 | 采购数量 |
| 14 | 规格 |
| 15 | 订货会员 |
| 16 | 序号 |
| 17 | 品牌/类目 |
| 18 | 商品基本信息 |
| 19 | 采购数量 |
| 20 | 规格 |
| 21 | 供应商 |
| 22 | 订货会员 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.startTime` |
| `rightTime` |
| `obj.customerKeyword` |
| `obj.keyword` |
| `companyIdArray[$index]` |
| `pageSize` |
| `item.purchaseRequestCount` |
| `item.supplierId` |
| `obj.purchaseRequestId` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getPurchaseRequestCountListFactory.count` |
| `corpInfo.` |
| `companyTitle` |
| `item.id` |
| `item.companyName` |
| `item.purchaseRequest.id` |
| `item.company.companyName` |
| `item.purchaseRequest.createName` |
| `item.purchaseRequest.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.purchaseRequest.productType` |
| `purchaseType` |
| `item.productNames` |
| `item.purchaseRequest.processStatus` |
| `processStatus` |
| `getStockTakingObjectFactory.object.purchaseRequest.createName` |
| `getStockTakingObjectFactory.object.purchaseRequest.checkName` |
| `detail.requestTime` |
| `detail.remark` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.purchaseRequestSku.skuCount` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.product.model1Name` |
| `item.purchaseRequestSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.purchaseRequestSku.model2` |
| `item.purchaseRequestSku.remark` |
| `item.purchaseRequestSku.customerInfo.customerName` |
| `item.purchaseRequestSku.customerInfo.companyName` |
| `totalCount` |
| `item.productSku.model1` |
| `item.productSku.model2` |
| `item.purchaseRequestSkuRemark` |
| `item.purchaseRequestSkuCustomerInfo.customerName` |
| `item.purchaseRequestSkuCustomerInfo.companyName` |
| `totalPurchaseCount` |
| `len` |
| `orderLength` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setTab(null)` |
| `setTab(0)` |
| `setTab(1)` |
| `createOrder()` |
| `open1()` |
| `open2()` |
| `setType(null)` |
| `setType(1)` |
| `setType(2)` |
| `searchAllCateId()` |
| `selectAll($event)` |
| `updateSelection($event,item.purchaseRequest.id)` |
| `showCheckDetail(item.purchaseRequest.id)` |
| `deleteStock(item.purchaseRequest.id)` |
| `viewSaleModal=false;` |
| `viewSaleModal=false` |
| `showOrder()` |
| `addSaleModal=false` |
| `selectOrderModal()` |
| `$close()` |

**跳转到**：`purchase.materialPurchase`, `purchase.materialPurchaseReturn`

**下拉数据源（ng-options）**

```
x.id as x.supplierName for x in  getSupplierListFactory.items
```

### 3.64 `purchaseRequestCheckDetail`

- **URL**：`/purchaseRequestCheckDetail?purchaseRequestId`
- **模板**：`views/materialAdmin/purchaseRequestCheckDetail.html`
- **控制器**：`purchaseRequestCheckDetailCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品规格信息 |
| 4 | 采购数量 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `purchase.requestTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `purchase.remark` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.productSku.model1` |
| `item.productSku.model2` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.purchaseRequestSku.skuCount` |
| `totalCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |

**跳转到**：`purchase.purchaseRequestCheck`

### 3.65 `purchaseRequestDetail`

- **URL**：`/purchaseRequestDetail?purchaseRequestId`
- **模板**：`views/materialAdmin/purchaseRequestDetail.html`
- **控制器**：`purchaseRequestModifyCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品基本信息 |
| 4 | 规格 |
| 5 | 订货会员 |
| 6 | 采购数量 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockTakingObjectFactory.object.purchaseRequest.createName` |
| `getStockTakingObjectFactory.object.purchaseRequest.checkName` |
| `purchase.requestTime` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `purchase.remark` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.product.model1Name` |
| `item.purchaseRequestSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.purchaseRequestSku.model2` |
| `item.purchaseRequestSku.remark` |
| `item.purchaseRequestSku.customerInfo.customerName` |
| `item.purchaseRequestSku.customerInfo.companyName` |
| `item.purchaseRequestSku.skuCount` |
| `totalCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |

**跳转到**：`materialPurchaseRequest`

### 3.66 `purchaseRequestModify`

- **URL**：`/purchaseRequestModify?purchaseRequestId`
- **模板**：`views/materialAdmin/purchaseRequestModify.html`
- **控制器**：`purchaseRequestModifyCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品基本信息 |
| 4 | 采购数量 |
| 5 | 规格 |
| 6 | 订货信息 |
| 7 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `purchase.requestTime` |
| `purchase.remark` |
| `item.purchaseRequestSku.skuCount` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockTakingObjectFactory.object.purchaseRequest.createName` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.product.model1Name` |
| `item.purchaseRequestSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.purchaseRequestSku.model2` |
| `item.purchaseRequestSku.remark` |
| `item.purchaseRequestSku.customerInfo.customerName` |
| `item.purchaseRequestSku.customerInfo.companyName` |
| `item.medicalProduct.useCount` |
| `item.medicalProduct.unitName` |
| `item.medicalProduct.refundCount` |
| `totalCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `open1()` |
| `deleteReceipt(item.purchaseRequestSku.id,$index)` |
| `saveInventory()` |
| `checkSupplier()` |

**跳转到**：`materialPurchaseRequest`

### 3.67 `goods.receiptCompanyDetail`

- **URL**：`/receiptCompanyDetail?stockInId`
- **模板**：`views/materialAdmin/receiptDetail.html`
- **控制器**：`receiptDetailCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getSkuCodeVoListOfStockIn` | `POST /admin/getSkuCodeVoListOfStockIn.json` |
| `getStockConf` | `POST /admin/getStockConf.json` |
| `getStockInSkuVoListOfStockIn` | `POST /admin/getStockInSkuVoListOfStockIn.json` |
| `getStockInVo` | `POST /admin/getStockInVo.json` |
| `selectCloudPrinterList` | `POST /admin/selectCloudPrinterList.json` |
| `sendSkuToCloudPrinter` | `POST /admin/sendSkuToCloudPrinter.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 生产厂家 |
| 6 | 生产许可证号 |
| 7 | 数量 |
| 8 | 成本价 |
| 9 | 成本合计 |
| 10 | 成本合计(￥) |
| 11 | 生产日期 |
| 12 | 批号/有效期 |
| 13 | 唯一标识码 |
| 14 | 状态 |
| 15 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `cloud.cloudPrinterId` |
| `keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.stockIn.id` |
| `obj.stockIn.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `obj.stockIn.createName` |
| `obj.stockIn.inDate` |
| `obj.stockIn.inType` |
| `inType` |
| `obj.supplier.supplierName` |
| `obj.storehouse.name` |
| `obj.stockIn.remark` |
| `obj.stockIn.checkDate` |
| `obj.stockIn.checkName` |
| `item.stockInSku.id` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.factory` |
| `item.productSku.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockInSku.remark` |
| `item.product.factoryLicense` |
| `item.stockInSku.skuCount` |
| `item.stockInSku.skuPrice` |
| `toFixed` |
| `item.stockInSku.skuTotalPrice` |
| `item.stockInSku.productionDate` |
| `item.stockInSku.batchNo` |
| `item.stockInSku.expiresDate` |
| `item.stockInSku.uniqueCode` |
| `item.stockInSku.checked` |
| `supplierChecked` |
| `totalprice` |
| `totalfee` |
| `item.skuCode` |
| `item.marketPrice` |
| `item.unitName` |
| `item.productName` |
| `item.model1` |
| `item.model2` |
| `val.id` |
| `val.remark` |
| `val.serialNumber` |

**页面动作（ng-click）**

| 动作 |
|---|
| `back()` |
| `printAll(1)` |
| `printQrcode(1)` |
| `hideSupplier()` |
| `printQrcode(2,item.stockInSku.id)` |
| `printAll(2,item.stockInSku.id)` |
| `printAllModel=false` |
| `selectPrintDevice()` |

**跳转到**：`goods.companyMaterialReceipts`, `materialReceipts`

### 3.68 `receiptDetail`

- **URL**：`/receiptDetail?stockInId`
- **模板**：`views/materialAdmin/receiptDetail.html`
- **控制器**：`receiptDetailCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getSkuCodeVoListOfStockIn` | `POST /admin/getSkuCodeVoListOfStockIn.json` |
| `getStockConf` | `POST /admin/getStockConf.json` |
| `getStockInSkuVoListOfStockIn` | `POST /admin/getStockInSkuVoListOfStockIn.json` |
| `getStockInVo` | `POST /admin/getStockInVo.json` |
| `selectCloudPrinterList` | `POST /admin/selectCloudPrinterList.json` |
| `sendSkuToCloudPrinter` | `POST /admin/sendSkuToCloudPrinter.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 生产厂家 |
| 6 | 生产许可证号 |
| 7 | 数量 |
| 8 | 成本价 |
| 9 | 成本合计 |
| 10 | 成本合计(￥) |
| 11 | 生产日期 |
| 12 | 批号/有效期 |
| 13 | 唯一标识码 |
| 14 | 状态 |
| 15 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `cloud.cloudPrinterId` |
| `keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.stockIn.id` |
| `obj.stockIn.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `obj.stockIn.createName` |
| `obj.stockIn.inDate` |
| `obj.stockIn.inType` |
| `inType` |
| `obj.supplier.supplierName` |
| `obj.storehouse.name` |
| `obj.stockIn.remark` |
| `obj.stockIn.checkDate` |
| `obj.stockIn.checkName` |
| `item.stockInSku.id` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.factory` |
| `item.productSku.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockInSku.remark` |
| `item.product.factoryLicense` |
| `item.stockInSku.skuCount` |
| `item.stockInSku.skuPrice` |
| `toFixed` |
| `item.stockInSku.skuTotalPrice` |
| `item.stockInSku.productionDate` |
| `item.stockInSku.batchNo` |
| `item.stockInSku.expiresDate` |
| `item.stockInSku.uniqueCode` |
| `item.stockInSku.checked` |
| `supplierChecked` |
| `totalprice` |
| `totalfee` |
| `item.skuCode` |
| `item.marketPrice` |
| `item.unitName` |
| `item.productName` |
| `item.model1` |
| `item.model2` |
| `val.id` |
| `val.remark` |
| `val.serialNumber` |

**页面动作（ng-click）**

| 动作 |
|---|
| `back()` |
| `printAll(1)` |
| `printQrcode(1)` |
| `hideSupplier()` |
| `printQrcode(2,item.stockInSku.id)` |
| `printAll(2,item.stockInSku.id)` |
| `printAllModel=false` |
| `selectPrintDevice()` |

**跳转到**：`goods.companyMaterialReceipts`, `materialReceipts`

### 3.69 `receiptDetailCustomer`

- **URL**：`/receiptDetailCustomer?stockInId`
- **模板**：`views/materialAdmin/receiptDetailCustomer.html`
- **控制器**：`receiptDetailCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getSkuCodeVoListOfStockIn` | `POST /admin/getSkuCodeVoListOfStockIn.json` |
| `getStockConf` | `POST /admin/getStockConf.json` |
| `getStockInSkuVoListOfStockIn` | `POST /admin/getStockInSkuVoListOfStockIn.json` |
| `getStockInVo` | `POST /admin/getStockInVo.json` |
| `selectCloudPrinterList` | `POST /admin/selectCloudPrinterList.json` |
| `sendSkuToCloudPrinter` | `POST /admin/sendSkuToCloudPrinter.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品基本信息 |
| 4 | 规格 |
| 5 | 数量 |
| 6 | 成本合计(￥) |
| 7 | 批号/有效期 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.stockIn.id` |
| `obj.stockIn.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `obj.stockIn.createName` |
| `obj.stockIn.inDate` |
| `obj.stockIn.inType` |
| `inType` |
| `obj.supplier.supplierName` |
| `obj.storehouse.name` |
| `obj.stockIn.remark` |
| `obj.stockIn.checkDate` |
| `obj.stockIn.checkName` |
| `item.stockInSku.id` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.factory` |
| `item.productSku.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockInSku.remark` |
| `item.stockInSku.skuCount` |
| `item.stockInSku.batchNo` |
| `item.stockInSku.expiresDate` |
| `totalprice` |

**页面动作（ng-click）**

| 动作 |
|---|
| `back()` |
| `hideSupplier()` |

**跳转到**：`materialReceiptsCustomer`

### 3.70 `receiptInvalid`

- **URL**：`/receiptInvalid?stockInId`
- **模板**：`views/materialAdmin/receiptInvalid.html`
- **控制器**：`receiptInvalidCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `cancelStockIn` | `POST /admin/cancelStockIn.json` |
| `cancelStockInSku` | `POST /admin/cancelStockInSku.json` |
| `getStockInSkuVoListOfStockIn` | `POST /admin/getStockInSkuVoListOfStockIn.json` |
| `getStockInVo` | `POST /admin/getStockInVo.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 数量 |
| 6 | 成本合计(￥) |
| 7 | 生产日期 |
| 8 | 批号/有效期 |
| 9 | 状态 |
| 10 | 操作 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.stockIn.id` |
| `obj.stockIn.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `obj.stockIn.createName` |
| `obj.stockIn.inDate` |
| `obj.stockIn.inType` |
| `inType` |
| `obj.supplier.supplierName` |
| `obj.storehouse.name` |
| `obj.stockIn.remark` |
| `obj.stockIn.checkDate` |
| `obj.stockIn.checkName` |
| `item.stockInSku.id` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.factory` |
| `item.productSku.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockInSku.remark` |
| `item.stockInSku.skuCount` |
| `item.stockInSku.productionDate` |
| `item.stockInSku.batchNo` |
| `item.stockInSku.expiresDate` |
| `item.stockInSku.checked` |
| `supplierChecked` |
| `totalprice` |

**页面动作（ng-click）**

| 动作 |
|---|
| `back()` |
| `hideSupplier()` |
| `singleShow(item.stockInSku.id)` |
| `allShow()` |
| `modify()` |
| `hideModal()` |

**跳转到**：`goods.companyMaterialReceipts`, `materialReceipts`

### 3.71 `goods.receiptCompanyInvalid`

- **URL**：`/receiptCompanyInvalid?stockInId`
- **模板**：`views/materialAdmin/receiptInvalid.html`
- **控制器**：`receiptInvalidCtrl`
- **端点数**：4

**调用的端点**

| 动作 | 端点 |
|---|---|
| `cancelStockIn` | `POST /admin/cancelStockIn.json` |
| `cancelStockInSku` | `POST /admin/cancelStockInSku.json` |
| `getStockInSkuVoListOfStockIn` | `POST /admin/getStockInSkuVoListOfStockIn.json` |
| `getStockInVo` | `POST /admin/getStockInVo.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 数量 |
| 6 | 成本合计(￥) |
| 7 | 生产日期 |
| 8 | 批号/有效期 |
| 9 | 状态 |
| 10 | 操作 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `obj.stockIn.id` |
| `obj.stockIn.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `obj.stockIn.createName` |
| `obj.stockIn.inDate` |
| `obj.stockIn.inType` |
| `inType` |
| `obj.supplier.supplierName` |
| `obj.storehouse.name` |
| `obj.stockIn.remark` |
| `obj.stockIn.checkDate` |
| `obj.stockIn.checkName` |
| `item.stockInSku.id` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.factory` |
| `item.productSku.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.stockInSku.remark` |
| `item.stockInSku.skuCount` |
| `item.stockInSku.productionDate` |
| `item.stockInSku.batchNo` |
| `item.stockInSku.expiresDate` |
| `item.stockInSku.checked` |
| `supplierChecked` |
| `totalprice` |

**页面动作（ng-click）**

| 动作 |
|---|
| `back()` |
| `hideSupplier()` |
| `singleShow(item.stockInSku.id)` |
| `allShow()` |
| `modify()` |
| `hideModal()` |

**跳转到**：`goods.companyMaterialReceipts`, `materialReceipts`

### 3.72 `receiptModify`

- **URL**：`/receiptModify?stockInId`
- **模板**：`views/materialAdmin/receiptModify.html`
- **控制器**：`receiptModifyCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `checkStockIn` | `POST /admin/checkStockIn.json` |
| `computePrice` | `POST /admin/computePrice.json` |
| `getStockInSkuVoListOfStockIn` | `POST /admin/getStockInSkuVoListOfStockIn.json` |
| `getStockInVo` | `POST /admin/getStockInVo.json` |
| `updateStockInAndSkuList` | `POST /admin/updateStockInAndSkuList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 生产厂家 |
| 6 | 生产许可证号 |
| 7 | 数量 |
| 8 | 成本价 |
| 9 | 成本合计 |
| 10 | 批号 |
| 11 | 生产日期 |
| 12 | 有效期 |
| 13 | 唯一标识码 |
| 14 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.stockIn.inDate` |
| `obj.inType` |
| `obj.stockIn.inType` |
| `item.skuCount` |
| `item.skuPrice` |
| `item.skuTotalPrice` |
| `item.batchNo` |
| `item.productionDateLong` |
| `item.expiresDateLong` |
| `obj.stockIn.remark` |
| `tab.amount` |
| `tab.batchNo` |
| `tab.time` |
| `tab.time2` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockObjectFactory.object.stockIn.id` |
| `getStockObjectFactory.object.stockIn.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `getStockObjectFactory.object.stockIn.createName` |
| `obj.stockIn.inDate` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.model1Name` |
| `item.model1` |
| `printModel` |
| `item.model2Name` |
| `item.model2` |
| `item.remark` |
| `item.factoryLicense` |
| `item.uniqueCode` |
| `totalprice` |
| `totalfee` |
| `toFixed` |
| `getStockObjectFactory.object.storehouse.name` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideSupplier()` |
| `open1()` |
| `bindUdi.setShow(true)` |
| `bindUdi.allChoseFun()` |
| `setTab(1)` |
| `setTab(2)` |
| `setTab(4)` |
| `setTab(3)` |
| `bindUdi.choseSingle(item)` |
| `bindUdi.delListIndex($index)` |
| `modify(false)` |
| `modify(true)` |
| `open2()` |
| `setAllProduct()` |
| `setAllModal=false` |

**跳转到**：`goods.companyMaterialReceipts`, `materialReceipts`

**下拉数据源（ng-options）**

```
x.id as x.name for x in inType
```

### 3.73 `goods.receiptCompanyModify`

- **URL**：`/receiptCompanyModify?stockInId`
- **模板**：`views/materialAdmin/receiptModify.html`
- **控制器**：`receiptModifyCtrl`
- **端点数**：5

**调用的端点**

| 动作 | 端点 |
|---|---|
| `checkStockIn` | `POST /admin/checkStockIn.json` |
| `computePrice` | `POST /admin/computePrice.json` |
| `getStockInSkuVoListOfStockIn` | `POST /admin/getStockInSkuVoListOfStockIn.json` |
| `getStockInVo` | `POST /admin/getStockInVo.json` |
| `updateStockInAndSkuList` | `POST /admin/updateStockInAndSkuList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 生产厂家 |
| 6 | 生产许可证号 |
| 7 | 数量 |
| 8 | 成本价 |
| 9 | 成本合计 |
| 10 | 批号 |
| 11 | 生产日期 |
| 12 | 有效期 |
| 13 | 唯一标识码 |
| 14 | 操作 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.stockIn.inDate` |
| `obj.inType` |
| `obj.stockIn.inType` |
| `item.skuCount` |
| `item.skuPrice` |
| `item.skuTotalPrice` |
| `item.batchNo` |
| `item.productionDateLong` |
| `item.expiresDateLong` |
| `obj.stockIn.remark` |
| `tab.amount` |
| `tab.batchNo` |
| `tab.time` |
| `tab.time2` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockObjectFactory.object.stockIn.id` |
| `getStockObjectFactory.object.stockIn.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `getStockObjectFactory.object.stockIn.createName` |
| `obj.stockIn.inDate` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.model1Name` |
| `item.model1` |
| `printModel` |
| `item.model2Name` |
| `item.model2` |
| `item.remark` |
| `item.factoryLicense` |
| `item.uniqueCode` |
| `totalprice` |
| `totalfee` |
| `toFixed` |
| `getStockObjectFactory.object.storehouse.name` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideSupplier()` |
| `open1()` |
| `bindUdi.setShow(true)` |
| `bindUdi.allChoseFun()` |
| `setTab(1)` |
| `setTab(2)` |
| `setTab(4)` |
| `setTab(3)` |
| `bindUdi.choseSingle(item)` |
| `bindUdi.delListIndex($index)` |
| `modify(false)` |
| `modify(true)` |
| `open2()` |
| `setAllProduct()` |
| `setAllModal=false` |

**跳转到**：`goods.companyMaterialReceipts`, `materialReceipts`

**下拉数据源（ng-options）**

```
x.id as x.name for x in inType
```

### 3.74 `stockChange`

- **URL**：`/stockChange`
- **模板**：`views/materialAdmin/stockChange.html`
- **控制器**：`stockChangeCtrl`
- **端点数**：8

**调用的端点**

| 动作 | 端点 |
|---|---|
| `completeStockTransfer` | `POST /admin/completeStockTransfer.json` |
| `deleteStockTransfer` | `POST /admin/deleteStockTransfer.json` |
| `getCorpInfo` | `POST /admin/getCorpInfo.json` |
| `getStockTransferProductVoList` | `POST /admin/getStockTransferProductVoList.json` |
| `getStockTransferVo` | `POST /admin/getStockTransferVo.json` |
| `getStockTransferVoList` | `POST /admin/getStockTransferVoList.json` |
| `isAdminRoleStateOK` | `POST /admin/isAdminRoleStateOK.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 调拨单号 |
| 2 | 调出仓库 |
| 3 | 调入仓库 |
| 4 | 调出日期 |
| 5 | 制单人 |
| 6 | 类型 |
| 7 | 状态 |
| 8 | 操作 调拨出库时由调出仓管理员确认后审核，调拨入库时由调入仓管理员确认后入库 |
| 9 | 序号 |
| 10 | 名称 |
| 11 | 规格 |
| 12 | 零售价/单位 |
| 13 | 调拨数量 |
| 14 | 生产厂商 |
| 15 | 批号 |
| 16 | 有效期 |
| 17 | 序号 |
| 18 | 名称 |
| 19 | 规格 |
| 20 | 零售价/单位 |
| 21 | 调拨数量 |
| 22 | 生产厂商 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.outStorehouseId` |
| `obj.inStorehouseId` |
| `obj.outStartTime` |
| `rightTime` |
| `obj.keyword` |
| `obj.modelKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `tab` |
| `item.stockTransfer.id` |
| `item.outStorehouse.name` |
| `item.inStorehouse.name` |
| `item.stockTransfer.outDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.stockTransfer.createName` |
| `companyFactory.object.logo` |
| `companyFactory.object.corporationName` |
| `getCashflowObjectFactory.object.stockTransfer.id` |
| `getCashflowObjectFactory.object.stockTransfer.createName` |
| `getCashflowObjectFactory.object.outStorehouse.name` |
| `getCashflowObjectFactory.object.inStorehouse.name` |
| `getCashflowObjectFactory.object.stockTransfer.checkName` |
| `getCashflowObjectFactory.object.stockTransfer.operator` |
| `getCashflowObjectFactory.object.stockTransfer.remark` |
| `index` |
| `item.product.productName` |
| `item.productSku.model1` |
| `printModel` |
| `item.productSku.model2` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.stockTransferSku.transferCount` |
| `item.product.factory` |
| `item.outStockInSku.batchNo` |
| `item.outStockInSku.expiresDate` |
| `getProductTransferObjectFactory.object.stockTransfer.id` |
| `getProductTransferObjectFactory.object.stockTransfer.createName` |
| `getProductTransferObjectFactory.object.outStorehouse.name` |
| `getProductTransferObjectFactory.object.inStorehouse.name` |
| `getProductTransferObjectFactory.object.stockTransfer.checkName` |
| `getProductTransferObjectFactory.object.stockTransfer.operator` |
| `getProductTransferObjectFactory.object.stockTransfer.remark` |
| `item.stockTransferProduct.transferCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setProduct(1)` |
| `setProduct(2)` |
| `setTab(null)` |
| `setTab(0)` |
| `setTab(1)` |
| `setTab(2)` |
| `open1()` |
| `open2()` |
| `printProductList(item.stockTransfer.id)` |
| `printList(item.stockTransfer.id)` |
| `deleteStock(item.stockTransfer.id)` |

**跳转到**：`addStockChange`

**下拉数据源（ng-options）**

```
x.id as x.name for x in storehouseInArr
x.id as x.name for x in storehouseOutArr
```

### 3.75 `goods.stockCompanyChange`

- **URL**：`/stockCompanyChange`
- **模板**：`views/materialAdmin/stockChange.html`
- **控制器**：`stockChangeCtrl`
- **端点数**：8

**调用的端点**

| 动作 | 端点 |
|---|---|
| `completeStockTransfer` | `POST /admin/completeStockTransfer.json` |
| `deleteStockTransfer` | `POST /admin/deleteStockTransfer.json` |
| `getCorpInfo` | `POST /admin/getCorpInfo.json` |
| `getStockTransferProductVoList` | `POST /admin/getStockTransferProductVoList.json` |
| `getStockTransferVo` | `POST /admin/getStockTransferVo.json` |
| `getStockTransferVoList` | `POST /admin/getStockTransferVoList.json` |
| `isAdminRoleStateOK` | `POST /admin/isAdminRoleStateOK.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 调拨单号 |
| 2 | 调出仓库 |
| 3 | 调入仓库 |
| 4 | 调出日期 |
| 5 | 制单人 |
| 6 | 类型 |
| 7 | 状态 |
| 8 | 操作 调拨出库时由调出仓管理员确认后审核，调拨入库时由调入仓管理员确认后入库 |
| 9 | 序号 |
| 10 | 名称 |
| 11 | 规格 |
| 12 | 零售价/单位 |
| 13 | 调拨数量 |
| 14 | 生产厂商 |
| 15 | 批号 |
| 16 | 有效期 |
| 17 | 序号 |
| 18 | 名称 |
| 19 | 规格 |
| 20 | 零售价/单位 |
| 21 | 调拨数量 |
| 22 | 生产厂商 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.outStorehouseId` |
| `obj.inStorehouseId` |
| `obj.outStartTime` |
| `rightTime` |
| `obj.keyword` |
| `obj.modelKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `tab` |
| `item.stockTransfer.id` |
| `item.outStorehouse.name` |
| `item.inStorehouse.name` |
| `item.stockTransfer.outDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.stockTransfer.createName` |
| `companyFactory.object.logo` |
| `companyFactory.object.corporationName` |
| `getCashflowObjectFactory.object.stockTransfer.id` |
| `getCashflowObjectFactory.object.stockTransfer.createName` |
| `getCashflowObjectFactory.object.outStorehouse.name` |
| `getCashflowObjectFactory.object.inStorehouse.name` |
| `getCashflowObjectFactory.object.stockTransfer.checkName` |
| `getCashflowObjectFactory.object.stockTransfer.operator` |
| `getCashflowObjectFactory.object.stockTransfer.remark` |
| `index` |
| `item.product.productName` |
| `item.productSku.model1` |
| `printModel` |
| `item.productSku.model2` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.stockTransferSku.transferCount` |
| `item.product.factory` |
| `item.outStockInSku.batchNo` |
| `item.outStockInSku.expiresDate` |
| `getProductTransferObjectFactory.object.stockTransfer.id` |
| `getProductTransferObjectFactory.object.stockTransfer.createName` |
| `getProductTransferObjectFactory.object.outStorehouse.name` |
| `getProductTransferObjectFactory.object.inStorehouse.name` |
| `getProductTransferObjectFactory.object.stockTransfer.checkName` |
| `getProductTransferObjectFactory.object.stockTransfer.operator` |
| `getProductTransferObjectFactory.object.stockTransfer.remark` |
| `item.stockTransferProduct.transferCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setProduct(1)` |
| `setProduct(2)` |
| `setTab(null)` |
| `setTab(0)` |
| `setTab(1)` |
| `setTab(2)` |
| `open1()` |
| `open2()` |
| `printProductList(item.stockTransfer.id)` |
| `printList(item.stockTransfer.id)` |
| `deleteStock(item.stockTransfer.id)` |

**跳转到**：`addStockChange`

**下拉数据源（ng-options）**

```
x.id as x.name for x in storehouseInArr
x.id as x.name for x in storehouseOutArr
```

### 3.76 `stockChangeCheck`

- **URL**：`/stockChangeCheck?id`
- **模板**：`views/materialAdmin/stockChangeCheck.html`
- **控制器**：`stockChangeCheckCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 调拨数量 |
| 7 | 生产日期 |
| 8 | 批号 |
| 9 | 有效期 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `inDate` |
| `item.outCount` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getTransferFactory.result.object.stockTransfer.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `getTransferFactory.result.object.stockTransfer.createName` |
| `getTransferFactory.result.object.outStorehouse.name` |
| `getTransferFactory.result.object.stockTransfer.outDate` |
| `getTransferFactory.result.object.inStorehouse.name` |
| `obj.operator` |
| `obj.remark` |
| `obj.checkName` |
| `obj.checkDate` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `item.model1Name` |
| `item.model1` |
| `item.model2Name` |
| `item.model2` |
| `item.unLockExistSkuCount` |
| `item.outCount` |
| `item.productionDate` |
| `item.batchNo` |
| `item.expiresDate` |
| `totalExistCount` |
| `totalprice` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `open1()` |
| `modify()` |

**跳转到**：`goods.stockCompanyChange`, `stockChange`

### 3.77 `goods.stockCompanyChangeCheck`

- **URL**：`/stockCompanyChangeCheck?id&storehouseId`
- **模板**：`views/materialAdmin/stockChangeCheck.html`
- **控制器**：`stockChangeCheckCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 调拨数量 |
| 7 | 生产日期 |
| 8 | 批号 |
| 9 | 有效期 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `inDate` |
| `item.outCount` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getTransferFactory.result.object.stockTransfer.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `getTransferFactory.result.object.stockTransfer.createName` |
| `getTransferFactory.result.object.outStorehouse.name` |
| `getTransferFactory.result.object.stockTransfer.outDate` |
| `getTransferFactory.result.object.inStorehouse.name` |
| `obj.operator` |
| `obj.remark` |
| `obj.checkName` |
| `obj.checkDate` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `item.model1Name` |
| `item.model1` |
| `item.model2Name` |
| `item.model2` |
| `item.unLockExistSkuCount` |
| `item.outCount` |
| `item.productionDate` |
| `item.batchNo` |
| `item.expiresDate` |
| `totalExistCount` |
| `totalprice` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `open1()` |
| `modify()` |

**跳转到**：`goods.stockCompanyChange`, `stockChange`

### 3.78 `stockChangeDetail`

- **URL**：`/stockChangeDetail?id`
- **模板**：`views/materialAdmin/stockChangeDetail.html`
- **控制器**：`stockChangeDetailCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 调拨数量 |
| 7 | 生产日期 |
| 8 | 批号 |
| 9 | 有效期 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getTransferFactory.result.object.stockTransfer.createName` |
| `getTransferFactory.result.object.outStorehouse.name` |
| `getTransferFactory.result.object.inStorehouse.name` |
| `obj.operator` |
| `obj.remark` |
| `obj.checkName` |
| `obj.checkDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `item.model1Name` |
| `item.model1` |
| `item.model2Name` |
| `item.model2` |
| `item.unLockExistSkuCount` |
| `item.outCount` |
| `item.productionDate` |
| `item.batchNo` |
| `item.expiresDate` |
| `totalExistCount` |
| `totalprice` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |

**跳转到**：`goods.stockCompanyChange`, `stockChange`

### 3.79 `goods.stockCompanyChangeDetail`

- **URL**：`/stockCompanyChangeDetail?id`
- **模板**：`views/materialAdmin/stockChangeDetail.html`
- **控制器**：`stockChangeDetailCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 调拨数量 |
| 7 | 生产日期 |
| 8 | 批号 |
| 9 | 有效期 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getTransferFactory.result.object.stockTransfer.createName` |
| `getTransferFactory.result.object.outStorehouse.name` |
| `getTransferFactory.result.object.inStorehouse.name` |
| `obj.operator` |
| `obj.remark` |
| `obj.checkName` |
| `obj.checkDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `index` |
| `item.brandName` |
| `item.categoryName` |
| `item.productName` |
| `item.marketPrice` |
| `item.unitName` |
| `item.factory` |
| `item.skuCode` |
| `item.model1Name` |
| `item.model1` |
| `item.model2Name` |
| `item.model2` |
| `item.unLockExistSkuCount` |
| `item.outCount` |
| `item.productionDate` |
| `item.batchNo` |
| `item.expiresDate` |
| `totalExistCount` |
| `totalprice` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |

**跳转到**：`goods.stockCompanyChange`, `stockChange`

### 3.80 `goods.stockProductChangeCheck`

- **URL**：`/stockProductChangeCheck?id&storehouseId`
- **模板**：`views/materialAdmin/stockProductChangeCheck.html`
- **控制器**：`stockProductChangeCheckCtrl`
- **端点数**：0

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 调拨数量 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `inDate` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getTransferFactory.result.object.stockTransfer.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `getTransferFactory.result.object.stockTransfer.createName` |
| `getTransferFactory.result.object.outStorehouse.name` |
| `getTransferFactory.result.object.stockTransfer.outDate` |
| `getTransferFactory.result.object.inStorehouse.name` |
| `obj.operator` |
| `obj.remark` |
| `obj.checkName` |
| `obj.checkDate` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.factory` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.unLockExistSkuCount` |
| `item.stockTransferProduct.transferCount` |
| `totalExistCount` |
| `totalprice` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |
| `open1()` |
| `modify()` |

**跳转到**：`goods.stockCompanyChange`, `stockChange`

### 3.81 `goods.stockProductChangeDetail`

- **URL**：`/stockProductChangeDetail?id&storehouseId`
- **模板**：`views/materialAdmin/stockProductChangeDetail.html`
- **控制器**：`modifyStockProductChangeCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `commitStockTransferByProductSku` | `POST /admin/commitStockTransferByProductSku.json` |
| `getStockPurchaseVo` | `POST /admin/getStockPurchaseVo.json` |
| `getStockTransferProductVoList` | `POST /admin/getStockTransferProductVoList.json` |
| `getStockTransferVo` | `POST /admin/getStockTransferVo.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |
| `updateStockTransferByProductSku` | `POST /admin/updateStockTransferByProductSku.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 序号 |
| 2 | 品牌/类目 |
| 3 | 商品信息 |
| 4 | 规格 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 |
| 6 | 调拨数量 |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getTransferFactory.result.object.stockTransfer.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `getTransferFactory.result.object.stockTransfer.createName` |
| `getTransferFactory.result.object.outStorehouse.name` |
| `getTransferFactory.result.object.stockTransfer.outDate` |
| `getTransferFactory.result.object.inStorehouse.name` |
| `getTransferFactory.result.object.stockTransfer.inDate` |
| `obj.operator` |
| `obj.remark` |
| `getTransferFactory.result.object.stockTransfer.checkName` |
| `getTransferFactory.result.object.stockTransfer.checkDate` |
| `index` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.factory` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.unLockExistSkuCount` |
| `item.stockTransferProduct.transferCount` |
| `totalExistCount` |
| `totalprice` |

**页面动作（ng-click）**

| 动作 |
|---|
| `hideReceipt()` |

**跳转到**：`goods.stockCompanyChange`, `stockChange`

### 3.82 `viewStockList`

- **URL**：`/viewStockList`
- **模板**：`views/materialAdmin/viewStockList.html`
- **控制器**：`stockListCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getCategoryTree2Level` | `POST /admin/getCategoryTree2Level.json` |
| `getChildrenLinkAndCode` | `POST /admin/getChildrenLinkAndCode.json` |
| `getStockInSkuVo` | `POST /admin/getStockInSkuVo.json` |
| `getStockInSkuVoList` | `POST /admin/getStockInSkuVoList.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表单标签**

| 标签 |
|---|
| 按商品 按批号 按产品 按商品导出 按批号导出 按产品导出 全部 库存 定制 库存小于0 |
| 库存等于0 |
| 库存大于0 |
| 库存不足预警 |
| 库存上限预警 |
| 近有效期预警 |
| 过期预警 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 品牌/类目 |
| 2 | 商品信息 |
| 3 | 规格 |
| 4 | 默认供应商 |
| 5 | 可用数量 可用数量 = 剩余数量 - 下单锁定 如果是付款同时扣减库存，付款后库存扣减、锁定数量归零； 如果是发货或领料时扣减库存，发货或领料后库存扣减、锁定数量归零； 可以系统里设置里修改扣减库存时间点。 |
| 6 | 剩余数量 |
| 7 | 平均成本 平均成本 = 成本合计 ÷ 剩余数量 平均成本为入库成本汇总后取平均值，该字段与系统设置里的成本价含义不同 |
| 8 | 成本合计 |
| 9 | 品牌/类目 |
| 10 | 商品信息 |
| 11 | 规格 |
| 12 | 默认供应商 |
| 13 | 可用数量 可用数量 = 剩余数量 - 下单锁定 如果是付款同时扣减库存，付款后库存扣减、锁定数量归零； 如果是发货或领料时扣减库存，发货或领料后库存扣减、锁定数量归零； 可以系统里设置里修改扣减库存时间点。 |
| 14 | 剩余数量 |
| 15 | 平均成本 平均成本 = 成本合计 ÷ 剩余数量 平均成本为入库成本汇总后取平均值，该字段与系统设置里的成本价含义不同 |
| 16 | 成本合计 |
| 17 | 生产日期 |
| 18 | 批号 |
| 19 | 有效期 |
| 20 | 入库日期 |
| 21 | 入库仓库 |
| 22 | 入库供应商 |
| 23 | 操作 |
| 24 | 品牌/类目 |
| 25 | 产品信息 |
| 26 | 默认供应商 |
| 27 | 可用数量 可用数量 = 剩余数量 - 下单锁定 如果是付款同时扣减库存，付款后库存扣减、锁定数量归零； 如果是发货或领料时扣减库存，发货或领料后库存扣减、锁定数量归零； 可以系统里设置里修改扣减库存时间点。 |
| 28 | 剩余数量 |
| 29 | 平均成本 平均成本 = 成本合计 ÷ 剩余数量 平均成本为入库成本汇总后取平均值，该字段与系统设置里的成本价含义不同 |
| 30 | 成本合计 |
| 31 | 品牌/类目 |
| 32 | 商品信息 |
| 33 | 规格 |
| 34 | 默认供应商 |
| 35 | 剩余库存 |
| 36 | 入库数量 |
| 37 | 成本合计(￥) |
| 38 | 生产日期 |
| 39 | 批号 |
| 40 | 有效期 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.lessThanZero` |
| `obj.equalToZero` |
| `obj.moreThanZero` |
| `obj.countWarning` |
| `obj.highCountWarning` |
| `obj.nearExpiresWarning` |
| `obj.expiresWarning` |
| `obj.brandId` |
| `pageSize` |
| `obj.batchNoKeyword` |
| `obj.keyword` |
| `obj.model1Keyword` |
| `obj.model2Keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockListFactory.count` |
| `obj.storehouseId` |
| `province.id` |
| `province.brandName` |
| `item.root.categoryName` |
| `iten.root.categoryName` |
| `getStockListFactory.total.unLockExistCount` |
| `getStockListFactory.total.existCount` |
| `getStockListFactory.total.existCostPrice` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.mainSupplier.supplierName` |
| `item.unLockExistSkuCount` |
| `item.stockInSkuExistCount` |
| `item.avgStockInSkuExistCostPrice` |
| `item.stockInSkuExistCostPrice` |
| `item.stockInSku.batchNo` |
| `item.stockInSku.expiresDate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.stockInSku.remark` |
| `item.stockInSku.skuPrice` |
| `item.stockInSku.productionDate` |
| `item.stockIn.gmtCreate` |
| `item.storehouse.name` |
| `item.supplier.supplierName` |
| `item.stockInProductExistCount` |
| `item.avgStockInProductExistCostPrice` |
| `item.stockInProductExistCostPrice` |
| `getStockObjectFactory.result.object.stockIn.id` |
| `getStockObjectFactory.result.object.stockIn.createName` |
| `getStockObjectFactory.result.object.stockIn.inType` |
| `inType` |
| `getStockObjectFactory.result.object.supplier.supplierName` |
| `getStockObjectFactory.result.object.storehouse.name` |
| `getStockObjectFactory.result.object.stockIn.remark` |
| `getStockObjectFactory.result.object.stockIn.checkName` |
| `getStockObjectFactory.result.object.brand.brandName` |
| `getStockObjectFactory.result.object.category.categoryName` |
| `getStockObjectFactory.result.object.product.productName` |
| `getStockObjectFactory.result.object.productSku.marketPrice` |
| `getStockObjectFactory.result.object.productSku.unitName` |
| `getStockObjectFactory.result.object.product.factory` |
| `getStockObjectFactory.result.object.product.productCode` |
| `getStockObjectFactory.result.object.productSku.skuCode` |
| `getStockObjectFactory.result.object.product.model1Name` |
| `getStockObjectFactory.result.object.product.model2Name` |
| `getStockObjectFactory.result.object.stockInSku.remark` |
| `getStockObjectFactory.result.object.mainSupplier.supplierName` |
| `getStockObjectFactory.result.object.stockInSkuExistCount` |
| `getStockObjectFactory.result.object.stockInSku.skuCount` |
| `getStockObjectFactory.result.object.stockInSku.batchNo` |
| `modalName` |
| `model1Val` |
| `model2Val` |
| `item.existSkuCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setStockTab(1)` |
| `setStockTab(2)` |
| `setStockTab(3)` |
| `showDaochu($event)` |
| `setCustomer(null)` |
| `setCustomer(1)` |
| `setCustomer(2)` |
| `getstockList()` |
| `chooseCategory(` |
| `chooseCategory(item.root.id,false)` |
| `chooseCategoryId(iten.root.id,$event)` |
| `schoolListFactory.nextPage()` |
| `showStoreModal(item)` |
| `showDetail(item.stockInSku.id)` |
| `stockDetail=false` |
| `hideStoreModal()` |

**跳转到**：`viewStockList`, `viewStockList2`, `viewStockList3`

### 3.83 `viewStockList2`

- **URL**：`/viewStockList2`
- **模板**：`views/materialAdmin/viewStockList2.html`
- **控制器**：`stockListsCtrl`
- **端点数**：10

**调用的端点**

| 动作 | 端点 |
|---|---|
| `getBrandListOfProduct` | `POST /admin/getBrandListOfProduct.json` |
| `getCategoryTree2Level` | `POST /admin/getCategoryTree2Level.json` |
| `getChildrenLinkAndCode` | `POST /admin/getChildrenLinkAndCode.json` |
| `getLimitStorehouseListOfCorp` | `POST /admin/getLimitStorehouseListOfCorp.json` |
| `getProductSkuCountInStorehouseVoList` | `POST /admin/getProductSkuCountInStorehouseVoList.json` |
| `getProductSkuInVoList` | `POST /admin/getProductSkuInVoList.json` |
| `getStockInSkuVo` | `POST /admin/getStockInSkuVo.json` |
| `getStockInSkuVoList` | `POST /admin/getStockInSkuVoList.json` |
| `selectStorehouseExistSkuCountVoList` | `POST /admin/selectStorehouseExistSkuCountVoList.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表单标签**

| 标签 |
|---|
| 按商品 按批号 --> 全部 库存 定制 导出 库存小于0 |
| 库存大于0 |
| 库存预警 |
| 有效预警 |

**表格列**

| # | 列名 |
|--:|---|
| 1 | 品牌/类目 |
| 2 | 商品信息 |
| 3 | 规格 |
| 4 | 合计 |
| 5 | {{item.name}} |
| 6 | 可用数量 可用数量 = 剩余数量 - 下单锁定 如果是付款同时扣减库存，付款后库存扣减、锁定数量归零； 如果是发货或领料时扣减库存，发货或领料后库存扣减、锁定数量归零； 可以系统里设置里修改扣减库存时间点。 |
| 7 | 剩余数量 |
| 8 | 平均成本 平均成本 = 成本合计 ÷ 剩余数量 平均成本为入库成本汇总后取平均值，该字段与系统设置里的成本价含义不同 |
| 9 | 成本合计 |
| 10 | 品牌/类目 |
| 11 | 商品信息 |
| 12 | 规格 |
| 13 | 可用数量 可用数量 = 剩余数量 - 下单锁定 如果是付款同时扣减库存，付款后库存扣减、锁定数量归零； 如果是发货或领料时扣减库存，发货或领料后库存扣减、锁定数量归零； 可以系统里设置里修改扣减库存时间点。 |
| 14 | 剩余数量 |
| 15 | 平均成本 平均成本 = 成本合计 ÷ 剩余数量 平均成本为入库成本汇总后取平均值，该字段与系统设置里的成本价含义不同 |
| 16 | 成本合计 |
| 17 | 批次 |
| 18 | 品牌/类目 |
| 19 | 商品信息 |
| 20 | 规格 |
| 21 | 剩余库存 |
| 22 | 入库数量 |
| 23 | 成本合计(￥) |
| 24 | 批号 |
| 25 | 有效期 |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `obj.lessThanZero` |
| `obj.moreThanZero` |
| `obj.countWarning` |
| `obj.expiresWarning` |
| `obj.brandId` |
| `obj.keyword` |
| `pageSize` |
| `obj.model1Keyword` |
| `obj.model2Keyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `getStockListFactory.count` |
| `obj.storehouseId` |
| `province.id` |
| `province.brandName` |
| `item.root.categoryName` |
| `iten.root.categoryName` |
| `item.name` |
| `getStockListFactory.total.unLockExistCount` |
| `getStockListFactory.total.existCount` |
| `getStockListFactory.total.existCostPrice` |
| `item.brand.brandName` |
| `item.category.categoryName` |
| `item.product.productName` |
| `item.product.factory` |
| `item.productSku.marketPrice` |
| `item.productSku.unitName` |
| `item.product.productCode` |
| `item.productSku.skuCode` |
| `item.product.model1Name` |
| `item.productSku.model1` |
| `printModel` |
| `item.product.model2Name` |
| `item.productSku.model2` |
| `item.totalSkuExistCountVo.stockInSkuExistCount` |
| `items.stockInSkuExistCount` |
| `item.unLockExistSkuCount` |
| `item.stockInSkuExistCount` |
| `item.avgStockInSkuExistCostPrice` |
| `item.stockInSkuExistCostPrice` |
| `iten.modelName` |
| `iten.modelValue` |
| `item.stockInSku.remark` |
| `item.stockInSku.skuPrice` |
| `item.stockIn.gmtCreate` |
| `date` |
| `yyyy` |
| `MM` |
| `dd` |
| `item.storehouse.name` |
| `item.stockInSku.batchNo` |
| `item.supplier.supplierName` |
| `getStockObjectFactory.result.object.stockIn.id` |
| `getStockObjectFactory.result.object.stockIn.createName` |
| `getStockObjectFactory.result.object.stockIn.inType` |
| `inType` |
| `getStockObjectFactory.result.object.supplier.supplierName` |
| `getStockObjectFactory.result.object.storehouse.name` |
| `getStockObjectFactory.result.object.stockIn.remark` |
| `getStockObjectFactory.result.object.stockIn.checkName` |
| `getStockObjectFactory.result.object.brand.brandName` |
| `getStockObjectFactory.result.object.category.categoryName` |
| `getStockObjectFactory.result.object.product.productName` |
| `getStockObjectFactory.result.object.productSku.marketPrice` |
| `getStockObjectFactory.result.object.productSku.unitName` |
| `getStockObjectFactory.result.object.product.factory` |
| `getStockObjectFactory.result.object.product.productCode` |
| `getStockObjectFactory.result.object.productSku.skuCode` |
| `getStockObjectFactory.result.object.product.model1Name` |
| `getStockObjectFactory.result.object.product.model2Name` |
| `getStockObjectFactory.result.object.stockInSku.remark` |
| `getStockObjectFactory.result.object.stockInSkuExistCount` |
| `getStockObjectFactory.result.object.stockInSku.skuCount` |
| `getStockObjectFactory.result.object.stockInSku.batchNo` |
| `modalName` |
| `model1Val` |
| `model2Val` |
| `item.existSkuCount` |

**页面动作（ng-click）**

| 动作 |
|---|
| `setProduct(1)` |
| `setProduct(2)` |
| `setCustomer(null)` |
| `setCustomer(1)` |
| `setCustomer(2)` |
| `showDaochu($event)` |
| `getstockList()` |
| `chooseCategory(` |
| `chooseCategory(item.root.id,false)` |
| `chooseCategoryId(iten.root.id,$event)` |
| `schoolListFactory.nextPage()` |
| `showStoreModal(item.productSku.id,item.product.productName,item.productSku.model1,item.productSku.model2)` |
| `showDetail(item.stockInSku.id)` |
| `stockDetail=false` |
| `hideStoreModal()` |

**跳转到**：`viewStockList`, `viewStockList2`, `viewStockList3`

### 3.84 `viewStockList3`

- **URL**：`/viewStockList3`
- **模板**：`views/materialAdmin/viewStockList3.html`
- **控制器**：`stockListssCtrl`
- **端点数**：6

**调用的端点**

| 动作 | 端点 |
|---|---|
| `completeStockTransfer` | `POST /admin/completeStockTransfer.json` |
| `createPromotion` | `POST /admin/createPromotion.json` |
| `getStockCountForTwoDimensionalTable` | `POST /admin/getStockCountForTwoDimensionalTable.json` |
| `getStockTransferProductVoList` | `POST /admin/getStockTransferProductVoList.json` |
| `getStockTransferVo` | `POST /admin/getStockTransferVo.json` |
| `selectStorehouseVoList` | `POST /admin/selectStorehouseVoList.json` |

**表格列**

| # | 列名 |
|--:|---|
| 1 | {{getList.result.object.product[direction.xName]}} {{getList.result.object.product[direction.yName]}} |
| 2 | {{col}} |
| 3 | {{row}} |
| 4 | {{getList.result.object.product.model1Name}} {{getList.result.object.product.model2Name}} |
| 5 | {{col}} |
| 6 | {{row}} |

**数据绑定（ng-model / model）**

| 绑定 |
|---|
| `model.model1Keyword` |
| `model.model2Keyword` |
| `model.skuCodeKeyword` |

**展示字段（{{}} 插值）**

| 字段 |
|---|
| `choseShop.shopInfo.productName` |
| `choseShop.btnStr` |
| `choseShop.status` |
| `getList.result.object.product.model1Name` |
| `getList.result.object.product.model2Name` |
| `getList.result.object.product` |
| `direction.xName` |
| `direction.yName` |
| `col` |
| `row` |
| `iten.id` |
| `iten.stockInSkuExistCount` |
| `printModel` |

**页面动作（ng-click）**

| 动作 |
|---|
| `choseShop.callBack()` |
| `getEr()` |
| `daochu()` |

**跳转到**：`viewStockList`, `viewStockList2`, `viewStockList3`
