<template>
  <div class="table-container">
    <vab-query-form>
      <el-form
        ref="form"
        :model="queryForm"
        :inline="true"
        @submit.native.prevent
      >
        <el-form-item>
          <el-input v-model="queryForm.chinese_name" placeholder="标题" />
        </el-form-item>
        <el-form-item>
          <el-input v-model="queryForm.director" placeholder="导演" />
        </el-form-item>
        <el-form-item>
          <el-date-picker
            v-model="queryForm.date"
            type="daterange"
            range-separator="至"
            start-placeholder=""
          ></el-date-picker>
        </el-form-item>
        <el-form-item>
          <el-select v-model="queryForm.category" placeholder="类型">
            <el-option
              v-for="item in allTypes"
              :key="item"
              :label="item"
              :value="item"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-input v-model="queryForm.actor" placeholder="演员" />
        </el-form-item>
        <el-form-item>
          <el-button
            icon="el-icon-search"
            type="primary"
            native-type="submit"
            @click="handleQuery"
          >
            查询
          </el-button>
        </el-form-item>
      </el-form>
    </vab-query-form>

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
  </div>
</template>

<script>
  import { keywordSearch } from '@/api/keyword'
  export default {
    name: 'ComprehensiveTable',
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
        pageSize: 20,
        imageList: [],
        listLoading: true,
        layout: 'total, sizes, prev, pager, next, jumper',
        allTypes: [
          '',
          '科幻',
          '惊悚',
          '喜剧',
          '爱情',
          '奇幻',
          '战争',
          '犯罪',
          '剧情',
          '悬疑',
          '其他',
        ],
        total: 0,
        background: true,
        elementLoadingText: '正在加载...',
        queryForm: {
          pageNo: 1,
          chinese_name: '',
          date: '',
          director: '',
          category: '',
          actor: '',
        },
      }
    },
    computed: {
      height() {
        return this.$baseTableHeight()
      },
    },
    created() {
      this.fetchData()
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
      this.$baseNotify(`欢迎使用 Keyword Search 功能`, `${thisTime}！`)
    },
    beforeDestroy() {},
    mounted() {},
    methods: {
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
        this.fetchData(this.queryForm)
      },
      handleQuery() {
        this.queryForm.pageNo = 1
        this.fetchData(this.queryForm)
      },
      async fetchData() {
        this.listLoading = true
        console.log(this.queryForm)
        const { data, totalCount } = await keywordSearch(this.queryForm)
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
        })
        console.log(data)
        this.list = data
        data.forEach((item, index) => {
          this.imageList.push(item.imgurl)
        })
        this.total = totalCount
        setTimeout(() => {
          this.listLoading = false
        }, 500)
      },
    },
  }
</script>
