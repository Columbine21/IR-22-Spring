<template>
  <div class="upload-container">
    <el-row>
      <el-divider content-position="left">演示环境可能无法模拟上传</el-divider>
      <vab-upload
        ref="vabUpload"
        url="/upload"
        name="file"
        :limit="50"
        :size="2"
        @showResult="showResult"
      ></vab-upload>
      <el-button type="primary" @click="handleShow({ key: 'value' })">
        模拟上传
      </el-button>
    </el-row>
    <el-row v-if="showTable">
      <el-table
        ref="tableSort"
        v-loading="listLoading"
        :data="list"
        :element-loading-text="elementLoadingText"
        :height="height"
        @cell-dblclick="showDetail"
        @sort-change="tableSortChange"
      >
        <el-table-column show-overflow-tooltip label="序号" width="95">
          <template #default="scope">
            {{ scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column
          show-overflow-tooltip
          prop="chinese_name"
          label="电影名"
        ></el-table-column>
        <el-table-column show-overflow-tooltip label="封面图">
          <template #default="{ row }">
            <el-image
              v-if="imgShow"
              :preview-src-list="imageList"
              :src="row.imgurl"
            ></el-image>
          </template>
        </el-table-column>
        <el-table-column
          show-overflow-tooltip
          label="上映时间"
          prop="date"
          sortable
        ></el-table-column>
        <el-table-column
          show-overflow-tooltip
          label="导演"
          prop="director"
        ></el-table-column>
        <el-table-column show-overflow-tooltip label="类别">
          <template #default="{ row }">
            <el-tooltip
              :content="row.category"
              class="item"
              effect="dark"
              placement="top-start"
            >
              <el-tag :type="row.status | statusFilter">
                {{ row.category }}
              </el-tag>
            </el-tooltip>
          </template>
        </el-table-column>
        <el-table-column
          show-overflow-tooltip
          label="演员列表"
          prop="actor"
        ></el-table-column>
        <el-table-column show-overflow-tooltip label="操作">
          <template #default="{ row }">
            <el-button type="text" @click="showDetail(row)">查看详情</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-pagination
        :background="background"
        :current-page="queryForm.pageNo"
        :layout="layout"
        :page-size="pageSize"
        :total="total"
        @current-change="handleCurrentChange"
      ></el-pagination>
    </el-row>
  </div>
</template>

<script>
  import VabUpload from './components/vabupload'

  export default {
    name: 'Upload',
    components: {
      VabUpload,
    },
    filters: {
      statusFilter(status) {
        const statusMap = {
          published: 'success',
          draft: 'gray',
          deleted: 'danger',
        }
        return statusMap[status]
      },
    },
    data() {
      return {
        imgShow: true,
        list: [],
        pageSize: 10,
        imageList: [],
        listLoading: true,
        layout: 'total, sizes, prev, pager, next, jumper',
        total: 0,
        showTable: false,
        background: true,
        elementLoadingText: '正在加载...',
        queryForm: {
          pageNo: 1,
        },
      }
    },
    computed: {
      height() {
        return this.$baseTableHeight()
      },
    },
    created() {
      const hour = new Date().getHours()
      const thisTime =
        hour < 8
          ? '早上好'
          : hour <= 11
          ? '上午好'
          : hour <= 13
          ? '中午好'
          : hour < 18
          ? '下午好'
          : '晚上好'
      this.$baseNotify(`欢迎使用 Frame Search 功能`, `${thisTime}！`)
    },
    methods: {
      handleShow(data) {
        this.$refs['vabUpload'].handleShow(data)
      },
      tableSortChange() {
        const imageList = []
        console.log(this.$refs.tableSort)
        this.$refs.tableSort.tableData.forEach((item, index) => {
          imageList.push(item.imgurl)
        })
        console.log(imageList)
        this.imageList = imageList
      },
      showDetail(row) {
        window.open(row.download_url)
      },
      handleCurrentChange(val) {
        this.queryForm.pageNo = val
        this.list = this.totalResult.slice(
          (this.queryForm.pageNo - 1) * this.pageSize,
          this.queryForm.pageNo * this.pageSize
        )
      },
      showResult(response) {
        this.listLoading = true
        this.showTable = true
        const { data, totalCount } = response
        data.forEach((item, index) => {
          if (item.actor === '') {
            item.actor = '动漫无真人演员'
          }
          if (item.category === '') {
            item.category = '动漫番剧'
          }
          if (item.director === '') {
            item.director = 'Unknown'
          }
          if (item.date === '') {
            item.date = 'Null'
          }
          this.imageList.push(item.imgurl)
        })
        this.totalResult = data
        this.list = this.totalResult.slice(0, this.pageSize)
        this.total = totalCount
        setTimeout(() => {
          this.listLoading = false
        }, 500)
      },
    },
  }
</script>
